import numpy as np
import cv2
import time
from cv2 import VideoWriter, VideoWriter_fourcc, imread, resize
import datetime

#
# Load templates for matching 
#
GameStartTemplate = cv2.imread('images/start_template.png',0)
ScoreboardTemplate = cv2.imread('images/topBoardTemplate2.png',0)
ScoreDigitPics = []
for i in range(0,10):
    ScoreDigitPics.append((cv2.imread('images/score_digits/%d.png' % i,0), i))
CaptureDeviceNum = 2 # Note: this will change depending on the number of cameras you have attached
fourcc = cv2.VideoWriter_fourcc(*'XVID')
# Note: The video size must match the correct frame image size, or the video will not demultiplex
VideoWriterImageSize = (720,480)
VideoWriterFramesPerSec = 30.0

#
# Get both team scores from a scoreboard image
#
# Returns: Tuple of (ourScore, theirScore) 
#
def GetScoresFromScoreboard(frame):    
    threshold = 0.9
    f_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 

    #cv2.imshow('res', frame)

    ourScoreTuples = []
    theirScoreTuples = []

    for currentDigit in ScoreDigitPics:

        res = cv2.matchTemplate(f_gray, currentDigit[0], cv2.TM_CCOEFF_NORMED)
        loc = np.where( res >= threshold)

	#cv2.imshow('digit', currentDigit[0])
        #p = (106, 50)  #64,50
        #cv2.rectangle(frame, p, (p[0] + 35, p[1] + 30), (0,0,255), 2)
        #crop_img = frame[p[1]:p[1]+30, p[0]:p[0]+35]
        #now = datetime.datetime.now()
        #name = 'digits/%s.png' % now.strftime('%Y-%m-%d-%H-%M-%s')
        #cv2.imwrite(name, crop_img)

        for pt in zip(*loc[::-1]):
#           w, h = currentDigit[0].shape[::-1]
#           cv2.rectangle(frame, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
#           cv2.imshow('res', frame)

            digitAndX = (pt[0], currentDigit[1])

            if pt[0] > 155:
                theirScoreTuples.append(digitAndX)
            else:
                ourScoreTuples.append(digitAndX)
            
    theirScore = sorted(list(set(theirScoreTuples)), key=lambda obj: obj[0])
    ourScore = sorted(list(set(ourScoreTuples)), key=lambda obj: obj[0])

    theirScoreFinal = []
    ourScoreFinal = []

    pixelDeltaForScore = 10
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

    #cv2.imshow('res', frame)
    if len(theirScoreFinal) > 0 and len(ourScoreFinal) > 0:
        theirScoreInt = int(''.join(str(x) for x in theirScoreFinal))
        ourScoreInt = int(''.join(str(x) for x in ourScoreFinal))
        return ourScoreInt, theirScoreInt
    else:
        return None, None

def CheckForScoreboard(frame):
    threshold = 0.8

    f_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 
    res = cv2.matchTemplate(f_gray, ScoreboardTemplate, cv2.TM_CCOEFF_NORMED)
    loc = np.where( res >= threshold)
    totalPoints = 0
    firstPoint = None

    for pt in zip(*loc[::-1]):
        if totalPoints == 0:
            firstPoint = pt
        totalPoints += 1

    #print(totalPoints)

    if totalPoints > 270:
        # We have the full top of the scoreboard 
        w = 290
        h = 100
        crop_img = frame[firstPoint[1]:firstPoint[1]+h, firstPoint[0]:firstPoint[0]+w]
        #cv2.imshow('crop', crop_img)
        #cv2.imwrite('crop.png', crop_img)
        return crop_img

def DetectGameStart(frameset):
    
    w, h = GameStartTemplate.shape[::-1]
    threshold = 0.8
    hasStartScreen = False 
    
    for frame in frameset:
        f_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 
        res = cv2.matchTemplate(f_gray, GameStartTemplate, cv2.TM_CCOEFF_NORMED)
        loc = np.where( res >= threshold)
    
    totalPoints = 0
    for pt in zip(*loc[::-1]):
        totalPoints += 1
        #cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)

    #cv2.imwrite('res.png',img_rgb)
    return totalPoints > 0
    
def WriteScoreAndTime(data):
    f = open("scoreData-%s" % datetime.datetime.now(), "w+")
    for entry in data: 
        f.write(entry)
    f.close() 

def TryGetVideo():
    cap = cv2.VideoCapture(CaptureDeviceNum)

    # Define the codec and create VideoWriter object
    now = datetime.datetime.now()
    videoName = 'videos/junk-%s.avi' % now.strftime('%Y-%m-%d-%H-%M-%s')
    currentVideo = cv2.VideoWriter(videoName,fourcc, VideoWriterFramesPerSec, VideoWriterImageSize)
    previousFrame = None
    lastScoreboardCheck = datetime.datetime.now()
    scoreAndTime = []

    frameCount = 0
    while(cap.isOpened()):
	# Capture frame-by-frame
	ret, frame = cap.read()

	if ret==True:
        # write the frame
	    currentVideo.write(frame)
            frameCount += 1
            #cv2.imwrite('frame.png', frame)
            if frameCount % 60 == 0: 
                frameCount = 0
                # Check if the frame has a scoreboard
                if (datetime.datetime.now() - lastScoreboardCheck).total_seconds() >= 1:
                    lastScoreboardCheck = datetime.datetime.now()
                    scoreboard = None 
                    try:
                        #print("Checking for scoreboard")
                        scoreboard = CheckForScoreboard(frame)
                    except:
                        print("Something went wrong while checking for the scoreboard") 
		
                    if not (scoreboard is None):
                        try:
                            ours, theirs = GetScoresFromScoreboard(scoreboard)
                            if not (ours is None) and not (theirs is None):
                                print("Current score:")
                                print((ours, theirs))
                                scoreAndTime.append(((ours, theirs), datetime.datetime.now()))
                        except:
                            print("Something went wrong while getting the score from the scoreboard") 

	    cv2.imshow('frame',frame)
	    if cv2.waitKey(1) & 0xFF == ord('q'):
          WriteScoreAndTime(scoreAndTime)
		  break
	else:
	    break

    # When everything is done, release the capture
    currentVideo.release()
    cap.release()
    cv2.destroyAllWindows()


while(True):
    print("Looking for video feed...")
    try:
        TryGetVideo()
    except: 
	   print("Error while trying to get video")
    
    print("No video detected. Waiting 5 seconds...")
    time.sleep(5)
