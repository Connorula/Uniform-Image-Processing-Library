from PIL import Image,ImageFilter, ImageDraw
from pytesseract import image_to_string
import csv
import cv2
import sys
from math import *
import numpy as np
from skimage.transform import (hough_line, hough_line_peaks,
                               probabilistic_hough_line)
from skimage.feature import canny
from skimage import data
import matplotlib.pyplot as plt
from matplotlib import cm


# Random Testing - Ignore
# im = Image.open("testfile.png")
# pix = im.load()
# print(im.size)
# print(pix[10,10])
# myText = image_to_string(Image.open("readertest.png"))
# print(myText)

class uImageBlueprint(object):
    imageTypeName = ""
    fileType = ""

    subSections = {}
    # def getIntersection(line1, line2):
    #     s1 = numpy.array(line1[0])
    #     e1 = numpy.array(line1[1])
    #
    #     s2 = numpy.array(line2[0])
    #     e2 = numpy.array(line2[1])
    #
    #     a1 = (s1[1] - e1[1]) / (s1[0] - e1[0])
    #     b1 = s1[1] - (a1 * s1[0])
    #
    #     a2 = (s2[1] - e2[1]) / (s2[0] - e2[0])
    #     b2 = s2[1] - (a2 * s2[0])
    #
    #     if abs(a1 - a2) < sys.float_info.epsilon:
    #         return False
    #
    #     x = (b2 - b1) / (a1 - a2)
    #     y = a1 * x + b1
    #     return (x, y)

    def findSectionsLines(self):
        img = cv2.imread(r'C:\Users\user\Documents\2017-2018 Academic Year\CSC-630W\Uniform-Image-Processing-Library\src\scheduletest.png', 1)
        print(img)
        ret,thresh = cv2.threshold(img,127,255,0)
        im2, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        counter = 0
        for cnt in contours:
            M = cv2.moments(cnt)
            # print(M)
            counter+=1
            perimeter = cv2.arcLength(cnt,True)
        print(counter)
        # gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        # edges = cv2.Canny(gray,50,150,apertureSize = 3)
        # found_lines = cv2.HoughLines(edges,1,np.pi/180,100)
        # lines = np.arrange([found_lines.length, 4])
        # for rho,theta in found_lines[0]:
        #     int counter = 0;
        #     a = np.cos(theta)
        #     b = np.sin(theta)
        #     x0 = a*rho
        #     y0 = b*rho
        #     x1 = int(x0 + 1000*(-b))
        #     lines[counter][]
        #     y1 = int(y0 + 1000*(a))
        #     x2 = int(x0 - 1000*(-b))
        #     y2 = int(y0 - 1000*(a))


    # def findSectionsColors(self):
    #     # hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    #     # lower_range = np.array([178, 179, 0])
    #     # upper_range = np.array([255, 255, 255])

    def addSection(self, x1, y1, x2, y2, name):
        try:
            self.subSections[name].append([x1,y1,x2,y2])

        except KeyError:
            self.subSections[name] = []
            self.subSections[name].append([x1,y1,x2,y2])

    def __init__(self, imageTypeName, fileType):
        self.imageTypeName = imageTypeName
        self.fileType = fileType

    def processImage(imageBlueprint,fileName):
        image = Image.open(fileName)
        pix = image.load()
        size = image.size
        csvHeaders = []
        csvText = []
        maxLength = 1
        counter = 0

        with open('text.csv', "w") as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            for key in imageBlueprint.subSections:
                csvHeaders.append(key)

            writer.writerow(csvHeaders)

            for header in csvHeaders:
                if (len(imageBlueprint.subSections[header]) > maxLength):
                    maxLength = len(imageBlueprint.subSections[header])

            while(counter < maxLength):
                for header in csvHeaders:
                    if(counter < len(imageBlueprint.subSections[header])):

                        csvText.append(imageBlueprint.subSections[header][counter])
                    else:
                        csvText.append("")
                writer.writerow(csvText)
                csvText = []
                counter = counter + 1

test = uImageBlueprint("Connor","png")
test.findSectionsLines()
# test.addSection(0,0,1,1,"mathClass")
# test.addSection(2,2,3,3,"class")
# test.addSection(4,4,5,5,"mathClass")
processImage(test,"scheduletest.png")
# print(test.subSections)
