import datetime
import time
import os
import sys
from time import sleep

from gpiozero import Button
from picamera import PiCamera
from gpiozero import LED
from gpiozero import MotionSensor

# audio control
from pygame import mixer

# Email Notifications
import smtplib
import ssl
from email.mime.text import MIMEText
from email.utils import formataddr
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

############################################################
# Assigning hardware GPIO pins #
############################################################

camera = PiCamera()
button = Button(17)
button_led = LED(27)
IF_circuit = LED(22)
pir = MotionSensor(21)
camera.resolution = (1280, 720)

############################################################
# Parameters #
############################################################

Doorbell_SFX = "/home/pi/music/bell.mp3"

sender_email = 'smtppython246@gmail.com'
sender_name = 'DOORBELL_SYSTEM'

receiver_email = 'smtppython246@gmail.com'
receiver_name = 'HOME_USER'

# receiver_emails = ['smtppython246@gmail.com', 'smtppython246@gmail.com', 'smtppython246@gmail.com']
# receiver_names = ['1', '2', '3']
password = 'asdfasewfeaf'

# Email Body
email_body = '''
    Motion was detected at the front door!
'''

Cap_img_direct = '/home/pi/Images/'


############################################################
# Global Parameters #
############################################################

DISABLE_PIR_SENSOR = False
ENABLE_IF_LED = False
start = datetime.time(19, 0, 0)
end = datetime.time(6, 0, 0)


############################################################
# FUNCTIONS #
############################################################

# Enables sound effects to play through speaker #
class SoundEffect:
    def __init__(self, filepath):
        self.filepath = filepath

    def play(self):
        if self.filepath:
            sound = mixer.Sound(self.filepath)
            sound.play()


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


# Checks if its day or night to enable IF LEDs for video/image capturing #
def time_in_range():
    global ENABLE_IF_LED
    global start
    global end

    # If the time is within the range specified enable IF LEDs
    current = datetime.datetime.now().time()
    if start <= current <= end:
        ENABLE_IF_LED = True
        button_led.on()
    else:
        ENABLE_IF_LED = False
        button_led.off()


# Takes image after motion is detected, returns location of image for sending #
def pir_capture():
    print("Motion detected")
    data = time.strftime("%Y-%b-%d_(%H:%M:%S)")
    camera.capture('/home/pi/Images/%s.jpg' % data)
    camera.close()
    # return name of image file
    return data


# _______________________________________________ Cloud computing needed _______________________________________________
def stream():

    # Turn on IF LEDs for night time video streaming
    if ENABLE_IF_LED:
        IF_circuit.off()

    print('Stream is starting...')
    time.sleep(15)
    print('Stream connection shutting down...')
    # Once stream is complete turn off IF LEDs
    IF_circuit.on()
# _______________________________________________ Cloud computing needed _______________________________________________


# Main function of the smart doorbell system #
def doorbell():
    # Define global variable within function
    global DISABLE_PIR_SENSOR
    global ENABLE_IF_LED

    # Check time of day: when to activate IF LED's
    time_in_range()

    # Re-enable the pir sensor after it detects no more motion, for the next loop
    if pir.motion_detected is False:
        DISABLE_PIR_SENSOR = False

    # Checks conditional state of sensors

    # If pir sensor senses motion take image and send notification
    if pir.motion_detected and DISABLE_PIR_SENSOR is False:
        # Disables the PIR Sensor until it no longer detects motion
        DISABLE_PIR_SENSOR = True

        # Turn on IF LEDs to take night picture
        if ENABLE_IF_LED:
            IF_circuit.off()

        image = pir_capture()
        IF_circuit.on()

        email_user('Cap_img_direct'+image + '.jpg')

    # If button is pressed start the bi-directional stream
    if button.is_pressed:
        bell = SoundEffect(Doorbell_SFX)
        bell.play()
        button_led.blink(n=3)
        stream()


if __name__ == '__main__':
    try:
        print("Activating Doorbell PIR...")
        IF_circuit.on()
        button_led.off()
        while True:
            doorbell()

    except KeyboardInterrupt:
        print("Doorbell System: Shutting down...")
        exit()
