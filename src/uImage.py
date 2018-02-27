from PIL import Image,ImageFilter, ImageDraw
from pytesseract import image_to_string
import csv
import cv2
import sys
from math import *
import numpy as np
from pathlib import Path
import os

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

    def findSections(self,fileName,threshold,boxArea):
        self.subSections = {}
        img = cv2.imread(str(fileName))
        imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        #2nd argument is 240 for iCalendar
        #2nd argument is 127 for PA Schedules
        ret,thresh = cv2.threshold(imgray,threshold,255,0)
        im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, 4)
        counter = 0
        counterHeader = 0
        for cnt in contours:
            if(cv2.contourArea(cnt) > boxArea):
                coord = [cnt[0][0][0],cnt[0][0][1],cnt[2][0][0],cnt[2][0][1]]
                if(coord[2] - coord[0] > 10 and coord[3] - coord[1] > 10):
                    self.addSection(coord,counterHeader)
                    img = cv2.drawContours(img, contours, counter, (0,255,0), 10)
                    cv2.rectangle(img,(coord[0],coord[1]),(coord[0]+5,coord[1]+5),(255,0,0),3)
                    cv2.rectangle(img,(coord[2],coord[3]),(coord[2]+5,coord[3]+5),(0,0,255),3)
                    middleCoord = (int((coord[0] + coord[2])/2),int((coord[1]+coord[3])/2))
                    cv2.putText(img,str(counterHeader), middleCoord, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 255)
                    counterHeader += 1
                elif coord[2] - coord[0] > 0 and coord[3] - coord[1] > 0:
                    extLeft = tuple(cnt[cnt[:, :, 0].argmin()][0])
                    extRight = tuple(cnt[cnt[:, :, 0].argmax()][0])
                    extTop = tuple(cnt[cnt[:, :, 1].argmin()][0])
                    extBot = tuple(cnt[cnt[:, :, 1].argmax()][0])
                    coord = [extLeft[0],extTop[1],extRight[0],extBot[1]]
                    self.addSection(coord,counterHeader)
                    img = cv2.drawContours(img, contours, counter, (0,255,0), 10)
                    cv2.rectangle(img,(coord[0],coord[1]),(coord[0]+5,coord[1]+5),(255,0,0),3)
                    cv2.rectangle(img,(coord[2],coord[3]),(coord[2]+5,coord[3]+5),(0,0,255),3)
                    middleCoord = (int((coord[0] + coord[2])/2),int((coord[1]+coord[3])/2))
                    cv2.putText(img,str(counterHeader), middleCoord, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 255)
                    counterHeader += 1
            counter+=1
        showimg = Image.fromarray(img, 'RGB')
        showimg.save('test.png')

    # def findSectionsColors(self):
    #     # hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    #     # lower_range = np.array([178, 179, 0])
    #     # upper_range = np.array([255, 255, 255])

    def addSection(self, coordinates, name):
        if coordinates[2] - coordinates[0] > 0 and coordinates[3] - coordinates[1] > 0:
            try:
                self.subSections[name].append(coordinates)

            except KeyError:
                self.subSections[name] = []
                self.subSections[name].append(coordinates)
        else:
            print("Invalid coordinates")

    def removeSection(self, headerName, index):
        newSubSections = {}
        popSubSections = []
        if(index[0] == -1):
            for header in self.subSections:
                if header not in headerName:
                    newSubSections[header] = []
                    for values in self.subSections[header]:
                        newSubSections[header].append(values)
        else:
            for header in self.subSections:
                if header not in headerName:
                    newSubSections[header] = []
                    for values in self.subSections[header]:
                        newSubSections[header].append(values)
                else:
                    newSubSections[header] = []
                    indexCounter = 0
                    for values in self.subSections[header]:
                        if indexCounter not in index:
                            newSubSections[header].append(values)
                        indexCounter += 1

        for header in newSubSections:
            if len(newSubSections[header]) == 0:
                popSubSections.append(header)

        for header in popSubSections:
            newSubSections.pop(header,None)

        self.subSections = newSubSections

    def renameSection(self, headerName, newHeaderName):
        try:
            if newHeaderName not in self.subSections:
                self.subSections[newHeaderName] = self.subSections.pop(headerName)
            else:
                for coord in self.subSections[headerName]:
                    self.subSections[newHeaderName].append(coord)
                self.subSections.pop(headerName)
        except KeyError:
            return None

    def getSectionText(self, headerName, fileName, index):
        try:
            image = Image.open(fileName)
            im4 = image.crop((self.subSections[headerName][index][0],self.subSections[headerName][index][1],self.subSections[headerName][index][2],self.subSections[headerName][index][3]))
            text = image_to_string(im4)
            return text
        except FileNotFoundError:
            print("File not found.")
            return None
        except KeyError:
            print("Dictionary does not contain this key")
            return None
        except IndexError:
            print("Index out of range")
            return None

    def __init__(self, imageTypeName, fileType):
        self.imageTypeName = imageTypeName
        self.fileType = fileType

    def processImage(self,imageFile,csvFile):
        try:
            image = Image.open(imageFile)
        except FileNotFoundError:
            print("File not found.")
            return None
        pix = image.load()
        size = image.size
        csvHeaders = []
        csvText = []
        maxLength = 1
        counter = 0

        my_file = Path(csvFile)
        if my_file.is_file():
            with open(csvFile, "a") as csv_file:
                writer = csv.writer(csv_file, delimiter=',')
                for key in self.subSections:
                    csvHeaders.append(key)

                for header in csvHeaders:
                    if (len(self.subSections[header]) > maxLength):
                        maxLength = len(self.subSections[header])

                while(counter < maxLength):
                    for header in csvHeaders:
                        if(counter < len(self.subSections[header])):
                            im3 = image.crop((self.subSections[header][counter][0],self.subSections[header][counter][1],self.subSections[header][counter][2],self.subSections[header][counter][3]))
                            csvText.append(image_to_string(im3))
                        else:
                            csvText.append("")
                    writer.writerow(csvText)
                    csvText = []
                    counter = counter + 1

        else:
            with open(csvFile, "w") as csv_file:
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
                            im3 = image.crop((self.subSections[header][counter][0],self.subSections[header][counter][1],self.subSections[header][counter][2],self.subSections[header][counter][3]))
                            csvText.append(image_to_string(im3))
                        else:
                            csvText.append("")
                    writer.writerow(csvText)
                    csvText = []
                    counter = counter + 1

    def processFolder(self,csvFile, path):
        folder = os.listdir( str(os.getcwd() + path) )
        for files in folder:
            if files[-(len(self.fileType)):] == self.fileType:
                print(files)
                print(str(os.getcwd() + "/" + files))
                self.processImage(str(os.getcwd() + path + "/" + files),csvFile)

test = uImageBlueprint("PASchedule","png")
# test.addSection([0,0,1,1],"bio")
# test.addSection([1,1,2,2],"bio")
test.addSection([500,2271,989,2578],"comp sci")
test.addSection([0,1325,495,1650],"mathClass")
# test.findSections("scheduletest.png",127,30000)
# test.removeSection(["bio","comp sci"],[5])
# print(test.subSections)
# test.renameSection("bio","comp sci")
print(test.subSections)
print(test.getSectionText("comp sci","scheduletest.png",0))
test.processImage("scheduletest.png","text.csv")
test.processFolder("newTest.csv", "")
