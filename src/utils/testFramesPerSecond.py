import numpy as np
import cv2
import time
from cv2 import VideoWriter, VideoWriter_fourcc, imread, resize
import datetime

cap = cv2.VideoCapture(2)

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'XVID')
now = datetime.datetime.now()
videoName = 'junk-%s.avi' % now.strftime('%Y-%m-%d-%H-%M-%s')

# Note: The video size must match the correct frame image size, or the video will not demultiplex
currentVideo = cv2.VideoWriter(videoName,fourcc, 30.0, (720,480))


frameCount = 0
start = datetime.datetime.now()
while(cap.isOpened()):
	# Capture frame-by-frame
	ret, frame = cap.read()
	frameCount += 1 
	current = datetime.datetime.now()

	timeDelta = (current - start).total_seconds()
	if timeDelta >= 5: 
		print("Time:")
		print(timeDelta)
		print("Frames:")
		print(frameCount)
		start = datetime.datetime.now()

currentVideo.release()
cap.release()
cv2.destroyAllWindows()
