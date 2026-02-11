import cv2
import numpy as np
try:
	from picamera2 import Picamera2			#if running on computer not connected to camera
except Exception as e:
	print(e)
import os
import matplotlib
import tkinter as tk
from tkinter import messagebox
import matplotlib.animation as anim
import time
import DoublePendulum_PivotMass as simulation
import PIL.Image, PIL.ImageTk

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

filename = 'Double_pendulum'
file_type = '.h264'

global cancel
cancel = False

# def record_video(video_length, width, height, fps):
# 	'''
# 	Args:
# 		filename (str):
# 			name of file to be created (without extension).
# 		video_length (int):
# 			length of video (seconds)
# 	'''
# 	try:
# 		with picamera2.PiCamera() as camera:
# 			camera.resolution = (width, height)
# 			camera.framerate = fps
# 			camera.shutter_speed = 1500
# 			camera.iso = 800
# 			time.sleep(2.1)
# 			camera.start_recording(filename + file_type)
# 			camera.wait_recording(video_length)
# 			camera.stop_recording()
# 			print('iso: {}'.format(camera.iso))
# 			print('brightness: {} \ndigital_gain: {}\nanalog_gain: {}\nexposure_compensation:\
# {}\nexposure_mode {}\nexposure_speed: {}\nimage_effect: {}\nsensor_mode :{}'.format(camera.brightness, camera.digital_gain,
# camera.analog_gain, camera.exposure_compensation, camera.exposure_mode, camera.exposure_speed, camera.image_effect,
# camera.sensor_mode))
# 	except Exception as e:
# 		print(e)
		

def record_video(video_length, width, height, fps, camera_num, filename, file_type):
    '''
    Args:
        filename (str):
            name of file to be created (without extension).
        video_length (int):
            length of video (seconds)
    '''
    try:
		# create an instance of the Picamera2 class
		# basically, initialising the camera
        picam2 = Picamera2(camera_num=camera_num)
		
        # choosing right settings
        video_config = picam2.create_video_configuration(
            main={"size": (width, height)}, 
            controls={"FrameRate": fps}
        )
		
        # apply config to camera we initialised
        picam2.configure(video_config)
		
        # mimic original ISO and shutter_speed settings
        picam2.set_controls({
            "ExposureMode": False,     # disable auto-exposure
            "AnalogueGain": 8.0,       # sensitivity for light --> AG x 100 = ISO
            "ExposureTime": 1500       # Shutter speed --> exposed to light for 1500 microsecs
        })
		
        time.sleep(2.1)                # give camera time to adjust
		
        # start recording
        picam2.start_recording(filename + file_type)
        time.sleep(video_length)
        picam2.stop_recording()
		
        picam2.stop()
		
    except Exception as e:
        print(e)
