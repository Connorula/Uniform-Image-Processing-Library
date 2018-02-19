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
im = Image.open("scheduletest.png")
im2 = im.crop((0,489,240,636))
# pix = im.load()
# print(im.size)
# print(pix[10,10])
myText = image_to_string(im2)
print(myText)

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

    def findSections(self):
        img = cv2.imread(r'C:\Users\user\Documents\2017-2018 Academic Year\CSC-630W\Uniform-Image-Processing-Library\src\scheduletest.png')
        img2 = cv2.imread(r'C:\Users\user\Documents\2017-2018 Academic Year\CSC-630W\Uniform-Image-Processing-Library\src\scheduletest.png')
        imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(imgray, 127, 255, 0)
        im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        perimeter = np.arange(len(contours))
        counter = 0
        for cnt in contours:
            perimeter[counter] = cv2.arcLength(cnt,True)
            if perimeter[counter] > 500:
                print(perimeter[counter])
            counter+=1
        print(counter)
        counter2 = 0
        for x in range(len(contours)):
            if perimeter[x] > 700 and perimeter[x] < 1000:
                counter2+=1
                cv2.drawContours(img2, contours, x, (0,255,0), 10)
        period_coordinates = []
        for x in range(counter2):
            print(contours[x])
            print(contours[x][0])
            period_coordinates.append([])
            period_coordinates[x].append(contours[x][0])
            period_coordinates[x].append(contours[x][2])
            period_coordinates[x].append(contours[x][1])
            period_coordinates[x].append(contours[x][3])
        showimg = Image.fromarray(img2, 'RGB')
        showimg.save(r'C:\Users\user\Documents\2017-2018 Academic Year\CSC-630W\Uniform-Image-Processing-Library\src\periods.png')
        for x in range(len(period_coordinates)):
            self.addSection(period_coordinates[x], str(x))

    # def findSectionsColors(self):
    #     # hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    #     # lower_range = np.array([178, 179, 0])
    #     # upper_range = np.array([255, 255, 255])
    def readSectionContents():
        return "Work in Progress"

    def addSection(self, coordinates, name):
        try:
            self.subSections[name].append(coordinates)

        except KeyError:
            self.subSections[name] = []
            self.subSections[name].append(coordinates)

    def __init__(self, imageTypeName, fileType):
        self.imageTypeName = imageTypeName
        self.fileType = fileType

    def processImage(self,fileName):
        image = Image.open(fileName)
        pix = image.load()
        size = image.size
        csvHeaders = []
        csvText = []
        maxLength = 1
        counter = 0

        with open('text.csv', "w") as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            for key in self.subSections:
                csvHeaders.append(key)

            writer.writerow(csvHeaders)

            for header in csvHeaders:
                if (len(self.subSections[header]) > maxLength):
                    maxLength = len(self.subSections[header])

            while(counter < maxLength):
                for header in csvHeaders:
                    if(counter < len(self.subSections[header])):

                        csvText.append(self.subSections[header][counter])
                    else:
                        csvText.append("")
                writer.writerow(csvText)
                csvText = []
                counter = counter + 1

<<<<<<< HEAD
# test = uImageBlueprint("Connor","png")
# test.addSection(0,0,1,1,"mathClass")
# test.addSection(2,2,3,3,"class")
# test.addSection(4,4,5,5,"mathClass")
# processImage(test,"scheduletest.png")
# print(test.subSections)
=======
test = uImageBlueprint("Connor","png")
test.findSections()
test.processImage("scheduletest.png")
print(test.subSections)
>>>>>>> f4cafdab0de81ce03a9f2b77b5b3c997f5e8f4b0
