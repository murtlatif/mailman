from mailTemplate import mailTemplate

from email.message import EmailMessage
from email.headerregistry import Address
from string import Template

import os
import smtplib
import csv

EMAIL_ADDRESS = os.environ.get('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')

FROM_ADDRESS = Address('EngSci Club Mailer', 'engsci', 'skule.ca')

def create_email(from_address, to_address, subject, plaintext, html=None):
    msg = EmailMessage()
    msg['From'] = from_address
    msg['To'] = to_address
    msg['Subject'] = subject
    msg.set_content(plaintext)

    if html is not None:
        msg.add_alternative(html, subtype='html')

    return msg

def main():

    # open the mailing list and get a list of all the recipients
    with open('list1.csv') as csvfile:
        contacts = [{k: v for k, v in row.items()}
            for row in csv.DictReader(csvfile, delimiter=',')]

    # open the template 
    f = open('template.txt', 'r')
    t = Template(f.read())

    # substitute the template for each contact 
    for contact in contacts:
        msg = ''
        try:
            msg = t.substitute(contact)
            b = create_email(FROM_ADDRESS, contact['email'], 'test', msg)
            
            with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
                smtp.ehlo()
                smtp.starttls()
                smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                smtp.send_message(b)
        except:
            print('Contact is missing attributes.')
            return
        
        print(msg)

if __name__ == '__main__':
    main()
