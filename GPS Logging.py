import serial
from email.mime.text import MIMEText
import smtplib
ser = serial.Serial('COM10', 4800, timeout=5)

def email(recipient, subject, message, encoding='plain'):
    """Generate an email

    Generate an email from sa-ptl@teslamotors.com to recipient list with subject and content using smtp

    Keyword Arguments:
    recipient (string) -- recipient addresses seperated by commas
    subject (string) -- this is the subject of the email
    message (string) -- this is the content of the email
    """

    msg = MIMEText(message, encoding)
    msg['Subject'] = subject
    msg['From'] = "elliot.dahlin@gmail.com"
    msg['To'] = recipient

    mail_server = smtplib.SMTP('smtp.gmail.com', 587)
    mail_server.ehlo()
    """ exisiting bug in IT security allows emails to be sent without authentication,
    will probably need to implement this later

    mail_server.starttls()
    mail_server.ehlo()
    mail_server.login("sa-ptl@teslamotors.com", "2#EDptl!")
    """
    recipient_list = recipient.split(",")
    mail_server.sendmail("sa-ptl@teslamotors.com", recipient_list, msg.as_string())
    mail_server.close()

def create_message():
    """Create a message for an email.

    Args:
    sender: Email address of the sender.
    to: Email address of the receiver.
    subject: The subject of the email message.
    message_text: The text of the email message.

    Returns:
    An object containing a base64url encoded email object.
    """
    message = email.base64mime("")
    message['to'] = "elliot.dahlin@gmail.com"
    message['from'] = "huynhjennt@gmail.com"
    message['subject'] = "test"
    return {'raw': message.as_string()}

def send_message(service, user_id, message):
    """Send an email message.

    Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    message: Message to be sent.

    Returns:
    Sent Message.
    """
    try:
        message = (service.users().messages().send(userId=user_id, body=message)
                   .execute())
        print('Message Id: %s' % message['id'])
        return message
    except:
        print('An error occurred')


while True:
    email("elliot.dahlin@gmail.com", "test", "GPS: ")
    line = str(ser.readline())
    splitline = line.split(',')

    if "GPGGA" in splitline[0]:
        time = float(splitline[1])-70000

        stripped_lattitude = str()
        for i in range(0, len(splitline[2])):
            if splitline[2][i] != ".":
                stripped_lattitude += splitline[2][i]
        lattitude = stripped_lattitude[:2] + "." + stripped_lattitude[2:]
        lattitude_direction = splitline[3]

        stripped_longitude= str()
        for i in range(0, len(splitline[4])):
            if splitline[4][i] != ".":
                stripped_longitude += splitline[4][i]
        longitude = stripped_longitude[:3] + "." + stripped_longitude[3:]
        longitude_direction = splitline[5]

        print("Time: " + str(time) + "; " + str(lattitude) + str(lattitude_direction) +
              " " + str(longitude) + str(longitude_direction))
