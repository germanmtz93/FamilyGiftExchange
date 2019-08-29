
import smtplib
from string import Template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

MY_ADDRESS = 'garciafamilygiftexchange@gmail.com'
PASSWORD = 'SuperSecretPass123'

# Get Matches Dictionary
# from gift_exchange import gift_exchange
import gift_exchange

#  Reads the contacts File
def get_contacts(filename):
    """
    Return two lists names, emails containing names and email addresses read from a file specified by filename.
    """ 
    names = []
    emails = []
    with open(filename, mode='r', encoding='utf-8') as contacts_file:
        for a_contact in contacts_file:
            names.append(a_contact.split(',')[0])
            emails.append((a_contact.split(',')[1]).rstrip())
    return names, emails

# Reads the template file
def read_template(filename):
    """
    Returns a Template object comprising the contents of the file specified by filename.
    """
    
    with open(filename, 'r', encoding='utf-8') as template_file:
        template_file_content = template_file.read()
    return Template(template_file_content)

# Main Fnction
def main():
    names, emails = get_contacts('contacts.txt') # read contacts
    message_template = read_template('message.txt')

    # set up the SMTP server
    s = smtplib.SMTP(host='smtp.gmail.com', port=587)
    s.starttls()
    s.login(MY_ADDRESS, PASSWORD)

    matches = gift_exchange.gift_exchange()

    # For each contact, send the email:
    for name, email in zip(names, emails):
        msg = MIMEMultipart()       # create a message

        # add in the actual person name to the message template
        message = message_template.substitute(GIVER_NAME=name.title(), RECEIVER_NAME=str(matches[name]))

        # Prints out the message body for our sake
        print(message)

        # setup the parameters of the message
        msg['From'] = MY_ADDRESS
        msg['To'] = email
        msg['Subject'] = "Garcia Family Gift Exchange 2019"
        
        # add in the message body
        msg.attach(MIMEText(message, 'plain'))
        
        # send the message via the server set up earlier.
        s.send_message(msg)
        del msg
        
    # Terminate the SMTP session and close the connection
    s.quit()
    
if __name__ == '__main__':
    main()