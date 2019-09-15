from email.message import EmailMessage
from email.headerregistry import Address
from string import Template
from generate_newsletter import generate_newsletter

import argparse
import csv
import json
import os
import sys
import smtplib

EMAIL_ADDRESS = os.environ.get('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')
EMAIL_NAME = os.environ.get('EMAIL_NAME')
EMAIL_USER = os.environ.get('EMAIL_USER')
EMAIL_DOMAIN = os.environ.get('EMAIL_DOMAIN')
FROM_ADDRESS = Address(EMAIL_NAME, EMAIL_USER, EMAIL_DOMAIN)

# debug printing
debug = True

def debugPrint(*argv):
    if debug:
        print(*argv)

# creates an email in a sendable format
def create_email(from_address, to_address, subject, plaintext, html=None):
    msg = EmailMessage()
    msg['From'] = from_address
    msg['To'] = to_address
    msg['Subject'] = subject
    msg.set_content(plaintext)

    if html is not None:
        msg.add_alternative(html, subtype='html')

    return msg

# sends an email
def send_email(email):
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(email)
    except:
        print('An error occurred while trying to send an email.')
        exit(1)

# get a list of contacts from a csv file
def get_contacts(csvfile):
    return [{k: v for k, v in row.items()} for row in csv.DictReader(csvfile, delimiter=',')]

def sendPersonalizedMassEmail(subject, address_csv, plaintext_template_file, html_template_file=None):

    # open the mailing list and get a list of all the recipients
    # with open(address_csv_path) as csvfile:
    contacts = get_contacts(address_csv)

    # get the templates
    plaintext_template = Template(plaintext_template_file.read())

    if html_template_file:
        html_template = Template(html_template_file.read())

    # substitute the template for each contact 
    for contact in contacts:
        try:
            plaintext_msg = plaintext_template.substitute(contact)
            if html_template_file:
                html_msg = html_template.substitute(contact)

            email_msg = create_email(FROM_ADDRESS, contact['email'], subject, plaintext_msg, html_msg if html_template_file else None)
            
            print(email_msg)
            # send_email(email_msg)
        except:
            print('Contact is missing attributes.')
            return

class MailMan:

    def __init__(self):
        parser = argparse.ArgumentParser(
            description='Mail delivery service',
            usage='''mailman.py <command> [<args>]

The available commands are:
    newsletter      Send a newsletter to a list of emails
    deliver         Send personalized emails with varying attributes to a list of emails
''')

        parser.add_argument('command', help='Subcommand to run')
        args = parser.parse_args(sys.argv[1:2])
        if not hasattr(self, args.command):
            print('Unrecognized command.')
            parser.print_help()
            exit(1)
        
        getattr(self, args.command)()

    def newsletter(self):
        # create an arg parser for this command
        parser = argparse.ArgumentParser(
            description='Send a newsletter to the specified recipients',
            usage='mailman.py newsletter [-h] CSV JSON')
        parser.add_argument('recipients', metavar='CSV', type=argparse.FileType('r'))
        parser.add_argument('newsletter_data', metavar='JSON', type=argparse.FileType('r'))

        # only take the arguments for the command, not the file/command itself
        args = parser.parse_args(sys.argv[2:])

        # retrieve contacts from the recipients file
        recipients = get_contacts(args.recipients)

        # generate the newsletter content
        newsletter = generate_newsletter(args.newsletter_data)

        # close files
        args.newsletter_data.close()
        args.recipients.close()

        # send the newsletter to each recipient
        for recipient in recipients:
            newsletter_email = create_email(FROM_ADDRESS, recipient['email'], newsletter['subject'], newsletter['plaintext'], newsletter['html'])
            send_email(newsletter_email)
            debugPrint(f"sending newsletter to {recipient['email']}")
            

    def deliver(self):
        # create an arg parser for this command
        parser = argparse.ArgumentParser(
            description='Deliver a personalized email to a list of recipients',
            usage='mailman.py deliver [-h] [-p --plaintext] subj CSV PT [HTML]')

        parser.add_argument('-p', '--plaintext', dest='plaintext_only', action='store_true', help='send email as plaintext only')
        parser.add_argument('subject', metavar='subj')
        parser.add_argument('recipients', metavar='CSV', type=argparse.FileType('r'))
        parser.add_argument('pt_template', metavar='PT', type=argparse.FileType('r'))
        parser.add_argument('html_template', metavar='HTML', nargs='?', type=argparse.FileType('r'))

        # only take the arguments for the command, not the file/command itself
        args = parser.parse_args(sys.argv[2:])

        # add a requirement for the HTML template unless the plaintext_only argument is true
        if (not args.plaintext_only) and not(args.html_template):
            print('HTML template is required unless using --plaintext.')
            parser.print_help()

            # close files before exiting
            args.recipients.close()
            args.pt_template.close()
            exit(1)
            
        # retrieve contacts from recipients file
        recipients = get_contacts(args.recipients)

        # get the templates
        plaintext_template = Template(args.pt_template.read())

        if not args.plaintext_only:
            html_template = Template(args.html_template.read())

        # close files
        args.recipients.close()
        args.pt_template.close()
        args.html_template.close()

        for recipient in recipients:
            try:
                plaintext_msg = plaintext_template.substitute(recipient)

                html_msg = None
                if not args.plaintext_only:
                    html_msg = html_template.substitute(recipient)

                email = create_email(FROM_ADDRESS, recipient['email'], args.subject, plaintext_msg, html_msg)
                debugPrint(f"sending personalized mail to {recipient['email']}")
                send_email(email)
            except:
                print('Contact is missing attributes.')
                return

if __name__ == '__main__':
    MailMan()
