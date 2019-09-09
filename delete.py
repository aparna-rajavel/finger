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
from  pyfingerprint import PyFingerprint

def deletefromdatabase():
    conn = sqlite3.connect('/home/pi/Desktop/Biometric-Attendance-System-using-Python-and-Raspberry-pi-3-/attendance/app.db')
    curs = conn.cursor()
    curs.execute("DELETE FROM finger_store WHERE id = 'positionNumber'")
    conn.commit()
    conn.close()
## Deletes a finger from sensor
##


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
print('Currently used templates: ' + str(f.getTemplateCount()) +'/'+ str(f.getStorageCapacity()))

## Tries to delete the template of the finger
try:
    positionNumber = input('Please enter the template position you want to delete: ')
    positionNumber= int(positionNumber)
    if ( f.deleteTemplate(positionNumber) == True ):
        deletefromdatabase();
        print('Template deleted!')

except Exception as e:
    print('Operation failed!')
    print('Exception message: ' + str(e))
    exit(1)
