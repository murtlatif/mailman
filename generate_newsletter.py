from string import Template
import json

default_colors = ['#55acee', '#3b5998', '#dc3545', '#8856ff', '#25e47a']


# ========== GENERATE HTML CODE ==========
def generate_html_button(buttonObj, color):
    text = buttonObj['text']
    href = buttonObj['href']

    if not text:
        print('No button text provided.')
        return
    if not href:
        print('No button href provided.')
        return

    return """
        <table width="100%" border="0" cellspacing="0" cellpadding="0">
            <tbody><tr>
                <td>
                <table border="0" cellspacing="0" cellpadding="0">
                    <tbody><tr>
                    <td align="left" style="border-radius: 3px;" bgcolor="{bcolor}">
                        <a class="button raised" href="{bhref}" target="_blank" style="font-size: 14px; line-height: 14px; font-weight: 500; font-family: Helvetica, Arial, sans-serif; color: #ffffff; text-decoration: none; border-radius: 3px; padding: 10px 25px; border: 1px solid {bcolor}; display: inline-block;">
                        {btext}
                        </a>
                    </td>
                    </tr>
                </tbody></table>
                </td>
            </tr>
            </tbody></table>
        """.format(btext=text, bhref=href, bcolor=color)

def generate_html_card(card_num, img, color, headline, body, buttonObj):
    if img:
        img = f'<img align="center" width="600" style="border-radius: 3px 3px 0px 0px; width: 100%; max-width: 600px!important" class="hund" src="{img}">'

    button = ''
    if buttonObj:
        button = generate_html_button(buttonObj, color)

    return """\
        <!-- START CARD {cardnum} -->
        <tr>
        <td width="100%" valign="top" align="center" class="padding-container" style="padding-top: 0px!important; padding-bottom: 18px!important; mso-padding-alt: 0px 0px 18px 0px;">
            <table width="600" cellpadding="0" cellspacing="0" border="0" align="center" class="wrapper">
            <tbody><tr>
                <td>
                <table cellpadding="0" cellspacing="0" border="0">
                    <tbody><tr>
                    <td style="border-radius: 3px; border-bottom: 2px solid #d4d4d4;" class="card-1" width="100%" valign="top" align="center">
                        <table style="border-radius: 3px;" width="600" cellpadding="0" cellspacing="0" border="0" align="center" class="wrapper" bgcolor="#ffffff">
                        <tbody><tr>
                            <td align="center">
                            <table width="600" cellpadding="0" cellspacing="0" border="0" class="container">
                                <!-- START HEADER IMAGE -->
                                <tbody><tr>
                                <td align="center" class="hund ripplelink" width="600">
                                    {html_img}
                                </td>
                                </tr>
                                <!-- END HEADER IMAGE -->
                                <!-- START BODY COPY -->
                                <tr>
                                <td class="td-padding" align="left" style="font-family: 'Courier New', Courier, 'Lucida Sans Typewriter', 'Lucida Typewriter', monospace; color: {html_color}; color: {html_color}!important; font-size: 24px; line-height: 30px; padding-top: 18px; padding-left: 18px!important; padding-right: 18px!important; padding-bottom: 0px!important; mso-line-height-rule: exactly; mso-padding-alt: 18px 18px 0px 13px;">
                                    {html_headline}
                                </td>
                                </tr>
                                <tr>
                                <td class="td-padding" align="left" style="font-family: 'Courier New', Courier, 'Lucida Sans Typewriter', 'Lucida Typewriter', monospace; color: #212121!important; font-size: 16px; line-height: 24px; padding-top: 18px; padding-left: 18px!important; padding-right: 18px!important; padding-bottom: 0px!important; mso-line-height-rule: exactly; mso-padding-alt: 18px 18px 0px 18px;">
                                    {html_body}
                                </td>
                                </tr>
                                <!-- END BODY COPY -->
                                <!-- BUTTON -->
                                <tr>
                                <td align="left" style="padding: 18px 18px 18px 18px;">
                                    {html_button}
                                </td>
                                </tr>
                                <!-- END BUTTON -->
                            </tbody></table>
                            </td>
                        </tr>
                        </tbody></table>
                    </td>
                    </tr>
                </tbody></table>
                </td>
            </tr>
            </tbody></table>
        </td>
        </tr>
        <!-- END CARD {cardnum} -->
        """.format(cardnum=card_num, html_img=img, html_headline=headline, html_body=body, html_button=button, html_color=color)

# ========== GENERATE PLAINTEXT ========== 
def generate_plaintext_card(data):

    # Add a space at the end if a link exists
    if data['plaintext_link']:
        data['plaintext_link'] += '\n'

    return """\
{pt_headline}
{pt_body}

{pt_link}
""".format(pt_headline=data['headline'], pt_body=data['body'], pt_link=data['plaintext_link'])

# ========== FILL CONTENT TO TEMPLATE ========== 
def html_add_content_to_template(content, html_template):
    html_filled_message = Template(html_template.read()).safe_substitute({"html_content": content})
    html_template.close()
    return html_filled_message

def plaintext_add_content_to_template(content, plaintext_template):
    plaintext_filled_message = Template(plaintext_template.read()).substitute({"plaintext_content": content})
    plaintext_template.close()
    return plaintext_filled_message

# ========== GENERATE NEWSLETTER (MAIN) ========== 
def generate_newsletter(data_json):

    # read the data json to retrieve newsletter data
    newsletter_data = json.load(data_json)

    # keep track of plaintext/html messages and card numbers for html
    newsletter_body = ''
    plaintext_body = ''
    cardnum = 1

    # ensure all data is required present in newsletter_data
    for card in newsletter_data['cards']:
        if not 'img' in card:
            card['img'] = ''

        if not 'color' in card:
            card['color'] = default_colors[(cardnum - 1) % 5]

        if not 'headline' in card:
            print(f'No headline found in card #{cardnum}')
            return

        if not 'body' in card:
            print(f'No body found in card #{cardnum}')
            return

        if not 'button' in card:
            card['button'] = ''

        if not 'plaintext_link' in card:
            card['plaintext_link'] = ''

        newsletter_body += generate_html_card(cardnum, card['img'], card['color'], card['headline'], card['body'], card['button'])
        plaintext_body += generate_plaintext_card(card)
        cardnum += 1

    return {
        "subject": newsletter_data['subject'],
        "html": html_add_content_to_template(newsletter_body, open('templates/newsletter/news_template.html', 'r')),
        "plaintext": plaintext_add_content_to_template(plaintext_body, open('templates/newsletter/news_template.txt', 'r'))
    }