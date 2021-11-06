import sys

# Email Notifications
import smtplib
import ssl
from email.mime.text import MIMEText
from email.utils import formataddr
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders


############################################################
# Parameters #
############################################################

sender_email = 'fun09a@gmail.com'
sender_name = 'DOORBELL_SYSTEM'

receiver_email = 'fun09a@gmail.com'
receiver_name = 'HOME_USER'

# receiver_emails = ['smtppython246@gmail.com', 'smtppython246@gmail.com', 'smtppython246@gmail.com']
# receiver_names = ['1', '2', '3']
password = 'SEDEsupercool123!'

# Email Body
email_body = '''
    Motion was detected at the front door!
'''


############################################################
# FUNCTION #
############################################################

# Handles SMTP server connection and email notifications #
def email_user(f_name):
    print('Sending the email')

    # configuring email information
    msg = MIMEMultipart()
    msg['To'] = formataddr((receiver_name, receiver_email))
    msg['From'] = formataddr((sender_name, sender_email))
    msg['Subject'] = 'Hello %s, the system has detected motion' % receiver_name

    msg.attach(MIMEText(email_body, 'plain'))

    try:
        with open(f_name, 'rb') as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())

            encoders.encode_base64(part)

            part.add_header(
                "Content-Disposition",
                f"attachment; filename= {f_name}",
            )

            msg.attach(part)
    except Exception as e:
        print("The image attachment was not found")

    try:
        # Creating a SMTP session
        server = smtplib.SMTP('smtp.gmail.com', 587)
        # Encrypt email
        context = ssl.create_default_context()
        server.starttls(context=context)
        # log in
        server.login(sender_email, password)
        # send email
        server.sendmail(sender_email, receiver_email, msg.as_string())
        print('Email sent')
    except Exception as e:
        print('An error occurred')
    finally:
        print('Closing the server')
        server.quit()
        
        
# take command line argument as the image path name
# always in the second position
email_user(sys.argv[1])