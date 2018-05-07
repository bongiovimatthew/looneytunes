import numpy as np
import cv2
from matplotlib import pyplot as plt
import time
from cv2 import VideoWriter, VideoWriter_fourcc, imread, resize

#
# Get both team scores from a scoreboard image
#
# Returns: Tuple of (ourScore, theirScore) 
#
def GetScoresFromScoreboard(frame):
    digitPics = []
    for i in range(0,10):
        digitPics.append((cv2.imread('score_digits/%d.png' % i,0), i))
    
    threshold = 0.9
    f_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 

    ourScoreTuples = []
    theirScoreTuples = []
    
    for currentDigit in digitPics:
        res = cv2.matchTemplate(f_gray, currentDigit[0], cv2.TM_CCOEFF_NORMED)
        loc = np.where( res >= threshold)

        for pt in zip(*loc[::-1]):
            w, h = currentDigit[0].shape[::-1]
            cv2.rectangle(frame, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
            
            digitAndX = (pt[0], currentDigit[1])

            if pt[0] > 400:
                theirScoreTuples.append(digitAndX)
            else:
                ourScoreTuples.append(digitAndX)
            
    theirScore = sorted(list(set(theirScoreTuples)), key=lambda obj: obj[0])
    ourScore = sorted(list(set(ourScoreTuples)), key=lambda obj: obj[0])

    theirScoreFinal = []
    ourScoreFinal = []

    pixelDeltaForScore = 40
    previousTuple = None
    for scoreTuple in theirScore:
        if previousTuple is None or abs(previousTuple[0] - scoreTuple[0]) > pixelDeltaForScore:
            theirScoreFinal.append(scoreTuple[1])
        previousTuple = scoreTuple

    previousTuple = None
    for scoreTuple in ourScore:
        if previousTuple is None or abs(previousTuple[0] - scoreTuple[0]) > pixelDeltaForScore:
            ourScoreFinal.append(scoreTuple[1])
        previousTuple = scoreTuple

    cv2.imshow('res', frame)

    theirScoreInt = int(''.join(str(x) for x in theirScoreFinal))
    ourScoreInt = int(''.join(str(x) for x in ourScoreFinal))
    return (ourScoreInt, theirScoreInt)




def GetTheirScoreFromScoreboard(frame):
    p1 = (380,130)
    h = 85
    w = 310

    frame = frame[p1[1]:p1[1]+h, p1[0]:p1[0]+w]
    cv2.imshow('res', frame)
    cv2.waitKey(0)

def GetOurScoreFromScoreboard(frame):
    p1 = (30,130)
    h = 85
    w = 310

    frame = frame[p1[1]:p1[1]+h, p1[0]:p1[0]+w]
    cv2.imshow('res', frame)
    cv2.waitKey(0)

def GetShotClockFromScoreboard(frame):
    p1 = (530,45)
    h = 45
    w = 110

    frame = frame[p1[1]:p1[1]+h, p1[0]:p1[0]+w]
    #cv2.rectangle(frame, p1, (p1[0]+w, p1[1]+h), (0,0,255), 2)
    cv2.imshow('res', frame)
    cv2.waitKey(0)

def GetTimeFromScoreboard(frame):
    p1 = (230,45)
    h = 45
    w = 210

    frame = frame[p1[1]:p1[1]+h, p1[0]:p1[0]+w]
    cv2.imshow('res', frame)
    cv2.waitKey(0)

def GetQuarterFromScoreboard(frame):
    p1 = (85,45)
    h = 45
    w = 54

    crop_img = frame[p1[1]:p1[1]+h, p1[0]:p1[0]+w]
    cv2.imshow('res', crop_img)
    cv2.waitKey(0)




frame = cv2.imread('crop.png')
scores = GetScoresFromScoreboard(frame)
print(scores)
cv2.waitKey(0)