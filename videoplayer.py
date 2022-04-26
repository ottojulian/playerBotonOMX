#!/usr/bin/env python3
import RPi.GPIO as GPIO
import os
import sys

import subprocess
import logging
import threading
import time
from omxplayer.player import OMXPlayer
from pathlib import Path


from subprocess import Popen

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)


movie1 = ("/home/pi/Videos/testMapBox.mp4")
movie2 = ("/home/pi/Videos/ojoGif.avi")
#player = OMXPlayer(movie1, args='--no-osd --loop')
#player.pause()


last_state1 = True
last_state2 = True

input_state1 = True
input_state2 = True

quit_video = True
player = False

print('creando overlay')
os.system('sudo fbi -a /home/pi/Desktop/awakening.png')



while True:
	#print(GPIO.input(17))
	#Read states of inputs
	input_state1 = GPIO.input(17)
	input_state2 = GPIO.input(18)
	quite_video = GPIO.input(24)
	#os.system('cls' if os.name == 'nt' else 'clear')
	#If GPIO(17) is shorted to ground
	if input_state1 != last_state1:

		if (player and not input_state1):
			os.system('killall omxplayer.bin')
			player = OMXPlayer(movie1, args='--no-osd')
			time.sleep(player.duration())
			player = True
		elif not input_state1:
			player = OMXPlayer(movie1, args='--no-osd')
			time.sleep(player.duration())
			player = True

		os.system('cls' if os.name == 'nt' else 'clear')

	#If GPIO(18) is shorted to ground
	elif input_state2 != last_state2:

		if (player and not input_state2):
			os.system('killall omxplayer.bin')
			player = OMXPlayer(movie2, args='--no-osd')
			time.sleep(player.duration())
			player = True
		elif not input_state2:
			player = OMXPlayer(movie2, args='--no-osd')
			time.sleep(player.duration())
			player = True

	#If omxplayer is running and GPIO(17) and GPIO(18) are NOT shorted to ground
	elif (player and input_state1 and input_state2):
		os.system('killall omxplayer.bin')
		player = False
	#GPIO(24) to close omxplayer manually - used during debug
	if quit_video == False:
		os.system('killall omxplayer.bin')
		player = False

	#Set last_input states
	last_state1 = input_state1
	last_state2 = input_state2
	#os.system('cls' if os.name == 'nt' else 'clear')
