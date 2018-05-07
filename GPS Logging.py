import serial
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
ser = serial.Serial('COM7', 4800, timeout=5)
from_addr = "dodgesprintersecurealarm@gmail.com"
to_addr = "elliot.dahlin@gmail.com"
msg = MIMEMultipart()
msg['From'] = from_addr
msg['To'] = to_addr
subjects = {"gps_update": "Sprinter Update GPS"}

def email(subject, message):
    """Generate an email

    Generate an email from sa-ptl@teslamotors.com to recipient list with subject and content using smtp

    Keyword Arguments:
    recipient (string) -- recipient addresses seperated by commas
    subject (string) -- this is the subject of the email
    message (string) -- this is the content of the email
    """
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(from_addr, "red12089")
    msg.attach(MIMEText(message, 'plain'))
    msg['Subject'] = subjects[subject]
    text = msg.as_string()
    server.sendmail(from_addr, to_addr, text)
    server.quit()
while True:
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

        message = "Time: " + str(time) + "; " + str(lattitude) + str(lattitude_direction) + " " + str(longitude) + str(longitude_direction)

        email("gps_update", message)