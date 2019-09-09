#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
PyFingerprint
Copyright (C) 2015 Bastian Raschke <bastian.raschke@posteo.de>
All rights reserved.

"""
from flask import Flask, session, redirect, url_for, escape, request, render_template, flash
import sqlite3
import sys
import pyfingerprint
import I2C_LCD_driver
import time
import hashlib
from pyfingerprint import PyFingerprint
from gtts import gTTS
import os
from picamera import PiCamera
from time import sleep

## Enrolls new finger
##
while True:
## Tries to initialize the sensor
 try:
	 f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)

	 if ( f.verifyPassword() == False ):
		raise ValueError('The given fingerprint sensor password is wrong!')

 except Exception as e:
	print('The fingerprint sensor could not be initialized!')
	print('Exception message: ' + str(e))
	exit(1)

## Gets some sensor information
 print('Currently used templates: ' + str(f.getTemplateCount()))

## Tries to enroll new finger
 try:
	print('Waiting for finger...')

	## Wait that finger is read
	while ( f.readImage() == False ):
		pass

	## Converts read image to characteristics and stores it in charbuffer 1
	f.convertImage(0x01)

	## Checks if finger is already enrolled
	result = f.searchTemplate()
	positionNumber = result[0]
	if(positionNumber == -1):
		print('nomatch')
		camera = PiCamera()
		sleep(2)
		camera.capture('/home/pi/Desktop/image.jpg')
		

## Wait that finger is read again
	while ( f.readImage() == False ):
		pass

	## Converts read image to characteristics and stores it in charbuffer 2
	f.convertImage(0x02)

	f.loadTemplate(positionNumber, 0x01)
	

	## Downloads the characteristics of template loaded in charbuffer 1
	characterics = str(f.downloadCharacteristics(0x01)).encode('utf-8')
	o=str(characterics)
	## Hashes characteristics of template
	cre_hash = hashlib.sha256(characterics).hexdigest()
	conn = sqlite3.connect('/home/pi/Desktop/Biometric-Attendance-System-using-Python-and-Raspberry-pi-3-/attendance/app.db')
	curs = conn.cursor()
	if(curs.execute("SELECT * FROM finger_store WHERE hashval=='o'")):
		
	 print('fingerprint already exist '+str(positionNumber))
	 curs.execute("SELECT * FROM finger_store ")
	 rows = curs.fetchall()
	 pan=rows[positionNumber][0]
	 
	 q='welcome '+str(pan)
	 print(q)
	 tts = gTTS(q,lang='en')
	 tts.save("good.mp3")
	 os.system("mpg321 good.mp3")

	conn.commit()
	conn.close
	
 except Exception as e:
	print('Operation failed!')
	print('Exception message: ' + str(e))
	exit(1)
