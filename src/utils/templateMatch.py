import numpy as np
import cv2
from matplotlib import pyplot as plt
import time
from cv2 import VideoWriter, VideoWriter_fourcc, imread, resize

GameStartTemplate = cv2.imread('topBoardTemplate.png',0)
frame = cv2.imread('screen3.png')

w, h = GameStartTemplate.shape[::-1]
threshold = 0.8
hasStartScreen = False 
f_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 
res = cv2.matchTemplate(f_gray, GameStartTemplate, cv2.TM_CCOEFF_NORMED)
loc = np.where( res >= threshold)
totalPoints = 0
firstPoint = None

for pt in zip(*loc[::-1]):
    if totalPoints == 0:
        firstPoint = pt
    lastPoint = pt
    #cv2.rectangle(frame, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
    totalPoints += 1

if totalPoints > 2000:
    # We have the full top of the scoreboard 
    w = 730
    h = 290
    #cv2.rectangle(frame, firstPoint, (firstPoint[0] + w, firstPoint[1] + h), (0,0,255), 2)
    crop_img = frame[firstPoint[1]:firstPoint[1]+h, firstPoint[0]:firstPoint[0]+w]
    #cv2.imshow('frame', frame)
    cv2.imwrite('crop.png', crop_img)
    cv2.waitKey(0)

#cv2.imwrite('res.png',frame)
cv2.imshow('res.png', frame)
cv2.waitKey(0)
print(totalPoints)
