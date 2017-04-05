import numpy as np
import cv2
import math

lower_red0 = np.array([0,100,60])
upper_red0 = np.array([15,255,255])

lower_blazeorange = np.array([7, 204, 204])
upper_blazeorange = np.array([15, 255,255])

def pixelsToFeet(pixels):
	return int(20.019 * math.exp(-0.015 * pixels))

def findMostCircularContour(cnts):
	minContour = cnts[0]
	minContourDifference = 100000
	for cnt in cnts:
		contourArea = cv2.contourArea(cnt)
		if(contourArea > 1000):
			(x,y),radius = cv2.minEnclosingCircle(cnt)
			center = (int(x),int(y))
			radius = int(radius)
			circleArea = 3.14159 * radius * radius
			if (circleArea - contourArea) < minContourDifference:
				minContour = cnt
				minContourDifference = circleArea - contourArea
	return minContour

def findColorBuoy(frame, lower, upper, color, overlay):
	blur = cv2.GaussianBlur(frame,(5,5),0)
	hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)

	mask = cv2.inRange(hsv, lower, upper)
	if color is "Red":
		mask0 = cv2.inRange(hsv, lower_red0, upper_red0)
		mask = mask + mask0
		#cv2.imshow("output",mask)
	mask = cv2.erode(mask, None, iterations=2)
	mask = cv2.dilate(mask, None, iterations=2)
	(_, cnts, _) = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
	if(len(cnts) > 0):
		c = findMostCircularContour(cnts)
		if cv2.contourArea(c) < 500:
			return
		peri = cv2.arcLength(c, True)

		contours_x = 0
		contours_y = 0
		contours_count = 0
		for line in c:
			contours_count = contours_count + 1
			contours_x = contours_x + line[0][0]
			contours_y = contours_y + line[0][1]
		if(contours_count > 0):
			contours_x = contours_x / contours_count
			contours_y = contours_y / contours_count

			center = (contours_x,contours_y)
			cv2.circle(overlay,center,5,(255,0,200),-1)
		approx = cv2.approxPolyDP(c, 0.1 * peri, True)
		cv2.drawContours(overlay, [approx], -1, (255, 0, 150), 3)

		x,y,w,h = cv2.boundingRect(c)
		cv2.rectangle(overlay,(x,y),(x+w,y+h),(255,0,200),2)

		(x,y),radius = cv2.minEnclosingCircle(c)
		center = (int(x),int(y))
		radius = int(radius)
		cv2.circle(overlay,center,radius,(255,0,200),2)
		cv2.putText(overlay,color + " " + str(pixelsToFeet(radius)) + "ft",center, 1, 2,(255,255,255), 1,cv2.LINE_AA)
	return

def getLegHighPoints(boxPts):
	minY = 1000
	minX = -1
	for pair in boxPts:
		if pair[1] < minY:
			minY = pair[1]
			minX = pair[0]
	return (minX, minY)

def getRotatedRect(contour, overlay):
	rect = cv2.minAreaRect(contour)
	box = cv2.boxPoints(rect)
	box = np.int0(box)
	cv2.drawContours(overlay,[box],0,(255,255,255),2)
	return box

def findGate(frame, lower, upper, blazeOrange, overlay, draw_tf):
	blur = cv2.GaussianBlur(frame,(5,5),0)
	hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
	box = None
	bounding_box_width = 300
	bounding_box_height = 200
	x = 0
	y = 0 
	angle = None

	min_x = 9999
	min_y = 9999

	mask = cv2.inRange(hsv, lower_blazeorange ,upper_blazeorange)

	gray = cv2.bilateralFilter(mask, 11, 17, 17)
	edged = cv2.Canny(gray, 30, 200)
	im, contours, hierarchy = cv2.findContours(edged,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
	if len(contours) >= 2:
		if draw_tf:
			cv2.drawContours(overlay, contours, 0, (0,255,0), 3)
			cv2.drawContours(overlay, contours, 1, (0,255,0), 3)

		cnt = contours[0]
		box = getRotatedRect(cnt, overlay)
		if box is not None:
			leg1 = getLegHighPoints(box)
    		cnt = contours[1]
    		box = getRotatedRect(cnt, overlay)
    		leg2 = getLegHighPoints(box)

    		dy = None
    		dx = max(leg1[0], leg2[0]) - min(leg1[0], leg2[0])
    		if leg1[0] > leg2[0]:
    			dy = leg2[1] - leg1[1]
    		else:
    			dy = leg1[1] - leg2[1]

    		if math.tan(dy / (1.0 * dx)) < 0:
    			angle = math.degrees(math.tan(dy / (1.0 * dx))) - 360
    		else:
    			angle = math.degrees(math.tan(dy / (1.0 * dx)))
    		x_mid = min(leg1[0], leg2[0]) + dx / 2.0
    		y_mid = min(leg1[1], leg2[1]) + dy / 2.0

    		if x_mid < overlay.shape[0] / 2 - bounding_box_width:
    			x = -1
    		elif x_mid > overlay.shape[0] / 2 + bounding_box_width:
    			x = 1
    		if y_mid < overlay.shape[1] / 2 - bounding_box_height:
    			y = -1
    		elif y_mid > overlay.shape[1] / 2 + bounding_box_height:
    			x_mid = 1

    		if draw_tf:
    			cv2.line(overlay, leg1, leg2, (0,255,255), 2)

	elif len(contours) == 1:
		x = 0
		y = 0
		cnt = contours[0]
		box = getRotatedRect(cnt, overlay)

		for pair in box:
			if pair[0] < min_x:
				min_x = pair[0]
			if pair[1] < min_y:
				min_y = pair[1]
    	if min_x < overlay.shape[0] / 2 - bounding_box_width:
    		x = -1
    	elif min_x > overlay.shape[0] / 2 + bounding_box_width:
    		x = 1
   		if min_y < overlay.shape[1] / 2 - bounding_box_height:
   			y = -1
   		elif min_y > overlay.shape[1] / 2 + bounding_box_height:
   			x_mid = 1
	return x, y, angle
