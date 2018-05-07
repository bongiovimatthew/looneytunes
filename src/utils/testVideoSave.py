import numpy as np
import cv2
import time
from cv2 import VideoWriter, VideoWriter_fourcc, imread, resize
import datetime

cap = cv2.VideoCapture(1)

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'XVID')
now = datetime.datetime.now()
videoName = 'junk-%s.avi' % now.strftime('%Y-%m-%d-%H-%M-%s')
currentVideo = cv2.VideoWriter(videoName,fourcc, 60.0, (720,480))
previousFrame = None

frameCount = 0

while(cap.isOpened() and frameCount < 300):
	# Capture frame-by-frame
	ret, frame = cap.read()
	frameCount += 1
	#h, w, c = frame.shape

	if ret==True:
	        
	    # write the frame
	    currentVideo.write(frame)
	    
	    cv2.imshow('frame',frame)
	    if cv2.waitKey(1) & 0xFF == ord('q'):
		break
	else:
	    break

# When everything is done, release the capture
currentVideo.release()
cap.release()
cv2.destroyAllWindows()
