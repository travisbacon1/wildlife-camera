# Import modules

import RPi.GPIO as GPIO
import os
from os import path
from datetime import datetime
from time import sleep
from picamera import PiCamera
from brightpi import *

# Configure GPIO pins

GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
button_pin = 10
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 10 to be an input

PIR_pin = 11
GPIO.setup(PIR_pin, GPIO.IN)
iOld = GPIO.input(PIR_pin)

# Assign variables

image_directory_path = "/home/pi/Desktop/Wildlife_Camera_Images"
camera = PiCamera()
camera.rotation = 270
camera.color_effects = (128,128)
camera_sleep_time = 2
camera.resolution = (3280, 2464)
camera.sharpness = 100

brightPi = BrightPi()
LED_ALL = (1, 2, 3, 4, 5, 6, 7, 8)
LED_WHITE = LED_ALL[0:4]
LED_IR = LED_ALL[4:8]
ON = 1
OFF = 0

normal_flash = OFF
IR_flash = ON

if normal_flash == ON and IR_flash == ON:
	full_flash = ON
else:
	full_flash = OFF

# Check picture directory exists/create it
if path.exists(image_directory_path) == True:
	pass
else:
	print("Creating images folder")
	try:
		os.mkdir(str(image_directory_path))
	except OSError:
		print (f"Creation of the image directory {image_directory_path} failed")

# Create folder for today

date_today = datetime.now()
year = date_today.strftime("%Y")
month = date_today.strftime("%m")
day = date_today.strftime("%d")
date_today = year + "/" + month + "/" + day
today_directory = os.path.join(image_directory_path, date_today)

if path.exists(today_directory) == True:
	pass
else:
	print("Creating folder for today's images")
	try:
		os.makedirs(today_directory)
		print(f"New folder created for {date_today}")
	except OSError as e:
		print (f"Creation of the today's image directory {today_directory} failed: {e}")

def take_picture_motion(PIR_pin):
	time_stamp = datetime.now()
	time_stamp = time_stamp.strftime("%Y-%m-%d-%H-%M-%S")
	print("Motion detected at: ", time_stamp)
	camera.annotate_text = time_stamp
	if full_flash == ON:
		brightPi.set_led_on_off(LED_ALL, ON)
	else:
		brightPi.set_led_on_off(LED_WHITE, normal_flash)
		brightPi.set_led_on_off(LED_IR, IR_flash)
	print("Smile!")
	sleep(camera_sleep_time)
	camera.capture(str(today_directory + "/" + time_stamp + ".jpeg"))
	brightPi.set_led_on_off(LED_ALL, OFF)
	brightPi.reset()
	print("Picture taken")
	time.sleep(0.5)

def take_picture_button(button_pin):
	time_stamp = datetime.now()
	time_stamp = time_stamp.strftime("%Y-%m-%d-%H-%M-%S")
	print("Manual camera trigger at: ", time_stamp)
	camera.annotate_text = time_stamp
	if full_flash == ON:
		brightPi.set_led_on_off(LED_ALL, ON)
	else:
		brightPi.set_led_on_off(LED_WHITE, normal_flash)
		brightPi.set_led_on_off(LED_IR, IR_flash)
	print("Smile!")
	sleep(camera_sleep_time)
	camera.capture(str(today_directory + "/" + time_stamp + ".jpeg"))
	brightPi.set_led_on_off(LED_ALL, OFF)
	brightPi.reset()
	print("Picture taken")
	time.sleep(0.5)

print("Camera ready. Waiting for trigger")

try:
	GPIO.add_event_detect(PIR_pin, GPIO.RISING, callback=take_picture_motion)
	GPIO.add_event_detect(button_pin, GPIO.RISING, callback=take_picture_button)
	while 1:
		time.sleep(1)
except KeyboardInterrupt:
	print("Shutting down camera")
	GPIO.cleanup()
