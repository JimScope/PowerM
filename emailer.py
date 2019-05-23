import imaplib
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from email import message_from_bytes
import time
import config
import utilities

retry_delay = 180 # Magic Number ;)


# Send an email
def send(destinatario, subject, message=" ", adjunto=None, name=None):
    msg = MIMEMultipart()
    msg['From'] = config.email_user_name
    msg['To'] = destinatario
    msg['Subject'] = subject
    msg.attach(MIMEText(message,'plain'))

    if adjunto is not None:
        with open(adjunto, 'rb') as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload((attachment).read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition',
            "attachment; filename="+name)
        msg.attach(part)

    try:
        text = msg.as_string()
        # server = smtplib.SMTP("smtp.gmail.com", 587)
        server = smtplib.SMTP("smtp.nauta.cu", 25)
        server.ehlo()
        #server.starttls()
        server.login(config.email_user_name, config.email_password)
        server.sendmail(config.email_user_name, destinatario, text)
        server.quit()
    except smtplib.SMTPException as e:
        # In case of errors, wait, and then resend
        # Subject can help identify what function tried to send the email
        utilities.log("Send Email Error: " +
                      subject + ", " + str(e.args[0]))
        time.sleep(retry_delay)


# Read new emails for commands
def read():
    msgs = []
    messages = []
    # Connect to gmail and send credentials
    # imap_conn = imaplib.IMAP4_SSL("imap.gmail.com")
    imap_conn = imaplib.IMAP4("imap.nauta.cu")
    imap_conn.login(config.email_user_name, config.email_password)
    status1 = imap_conn.select("INBOX")[0]

    try:
        results = imap_conn.uid('search', None, '(UNSEEN)', 'SUBJECT', '"' + config.subject + '"')[1]

        if results == [b'']:
            # print("No Messages Found")
            return None
        else:
            for num in results[0].split():
                data = imap_conn.uid('fetch', num, '(RFC822)')[1]
                msgs.append(data)
                
            for msg in msgs:
                fullmsg = message_from_bytes(msg[0][1])
                email_from = fullmsg.get('from').split('>')[0].split('<')[1]
                if email_from not in config.white_list:
                    # Log security problems
                    pass
                else:
                    body = get_body(fullmsg).decode('utf-8').replace('\r\n', '')
                    messages.append((email_from, body))
            return messages

    except Exception as e:
        # In case of errors, wait, then try again
        error_message = "No arguments found with exception."
        if e.args[0]:
            error_message = e.args[0]
        utilities.log("Read Email Error: " + str(error_message))
        time.sleep(retry_delay)


def get_body(mensaje):
    if mensaje.is_multipart():
        return get_body(mensaje.get_payload(0))
    else:
        return mensaje.get_payload(None, True)


if __name__ == '__main__':
    print(read())
