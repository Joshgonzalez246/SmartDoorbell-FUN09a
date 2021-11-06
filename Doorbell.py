import datetime
import time
import os
import sys
from time import sleep
import subprocess

from gpiozero import Button
from picamera import PiCamera
from gpiozero import LED
from gpiozero import MotionSensor
from pushbullet import Pushbullet

# audio control
import pygame

pygame.init()
pygame.mixer.init()


############################################################
# Assigning hardware GPIO pins #
############################################################

camera = PiCamera()
button = Button(17)
button_led = LED(27)
IF_circuit = LED(20)
pir = MotionSensor(21)
camera.resolution = (1280, 720)
camera.framerate = 24

############################################################
# Parameters #
############################################################

Doorbell_SFX = "bell.mp3"

folder = "Images/"
format = ".jpg"

API_KEY = "o.RS15opDtGy7kphnjqAGGjLH5eY7PG3lx"

pb = Pushbullet(API_KEY)

website_URL = "https://www.SmartDoorbellWebApp.com/"

############################################################
# Global Parameters #
############################################################

DISABLE_PIR_SENSOR = False
ENABLE_IF_LED = False
start = datetime.time(19, 0, 0)
end = datetime.time(6, 0, 0)
MAX_VID = 12
CAMERA_INTERRUPT = False


############################################################
# FUNCTIONS #
############################################################

# Enables sound effects to play through speaker #
class SoundEffect:
    def __init__(self, filepath):
        self.filepath = filepath

    def play(self):
        if self.filepath:
            pygame.mixer.music.load(self.filepath)
            pygame.mixer.music.play()
            
            
# PushBullet notification and API integration #

def ring_notification():
    push = pb.push_link("Someone is trying to reach you", website_URL)
    
def motion_notification():
    push = pb.push_note("Motion Detected", "Someone is at your door")
    
#def sms_notification():
#    device = pb.devices[0]
#     push = pb.push_sms(device, "+61449556793", "Yo check yo door")
    

# Checks if its day or night to enable IF LEDs for video/image capturing #
def time_in_range():
    global ENABLE_IF_LED
    global start
    global end

    # If the time is within the range specified enable IF LEDs
    current = datetime.datetime.now().time()
    # if night time range turn on LED circuit
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
    camera.capture('Images/%s.jpg' % data)
    # return name of image file
    return data


# _________ Cloud computing needed _____________
def stream():
    print("The button has been pressed...")
    bell = SoundEffect(Doorbell_SFX)
    bell.play()
    button_led.blink(n=4)
        
    # Turn on IF LEDs for night time video streaming
    if ENABLE_IF_LED:
        IF_circuit.off()

    print('Stream is starting...')
    ring_notification()
    #sms_notification()
    
    time.sleep(10)
    print('Stream connection shutting down...')
    # Once stream is complete turn off IF LEDs
    IF_circuit.on()
# _______________________________________________ Cloud computing needed _______________________________________________


# Main function of the smart doorbell system #
def doorbell():
    # Define global variable within function
    global DISABLE_PIR_SENSOR
    global ENABLE_IF_LED
    CAMERA_INTERRUPT = False

    # Check time of day: when to activate IF LED's
    time_in_range()

    # Re-enable the pir sensor after it detects no more motion, for the next loop
    if pir.motion_detected is False:
        DISABLE_PIR_SENSOR = False

    # Checks conditional state of sensors
    
    time.sleep(0.1)

    # If pir sensor senses motion take image and send notification
    if pir.motion_detected and DISABLE_PIR_SENSOR is False:
        # Disables the PIR Sensor until it no longer detects motion
        DISABLE_PIR_SENSOR = True

        # Turn on IF LEDs to take night picture
        if ENABLE_IF_LED:
            IF_circuit.off()

        file_time = pir_capture()

        IF_circuit.on()
        
        file_path = folder + file_time + format
        
        motion_notification()

        # Notifcation with image attachment for SMTP and pushbullet API
        p = subprocess.Popen([sys.executable, 'user_email.py', file_path], stdout=subprocess.PIPE)
        p = subprocess.Popen([sys.executable, 'Pushbullet_image.py', file_path], stdout=subprocess.PIPE)
        p = subprocess.Popen([sys.executable, 'FileUpload.py', file_path, file_time], stdout=subprocess.PIPE)
        
        # Record 5 Second clip
        camera.start_preview()
        camera.start_recording('/home/pi/Doorbell/Videos/' + file_time + '.h264')
        print('Recording has started...')
        
        # Records a small clip and stops recording after timeout or
        # if the button is pressed
        timeout = MAX_VID
        timeout_start = time.time()
        while time.time() < timeout_start + timeout:
            if button.is_pressed:
                print('Recording has stopped...')
                CAMERA_INTERRUPT = True
                camera.stop_recording()
                camera.stop_preview()
                
                file_path = 'Videos/' + file_time + '.h264'
                p = subprocess.Popen([sys.executable, 'FileUpload.py', file_path, file_time], stdout=subprocess.PIPE)
                
                stream()
                
        if CAMERA_INTERRUPT is False:
            print('Recording has stopped...')
            camera.stop_recording()
            camera.stop_preview()
        
        # Test MP4 upload when clouf computing is available
        # p = subprocess.Popen([sys.executable, 'FileUpload.py', file_path, file_time], stdout=subprocess.PIPE)    
        
        print("System loop resetting")

    # If button is pressed start the bi-directional stream
    if button.is_pressed:
        stream()
        print("System loop resetting")


if __name__ == '__main__':
    try:
        print("Activating Doorbell PIR...")
        IF_circuit.on()
        button_led.off()
        while True:
            doorbell()

    except KeyboardInterrupt:
        print("Doorbell System: Shutting down...")
        # turn off all LEDS
        IF_circuit.off()
        button_led.off()
        exit()
