from PIL import Image,ImageFilter, ImageDraw
from pytesseract import image_to_string
import csv
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
    def findSections(self):

        # Constructing test image
        image = np.zeros((100, 100))
        idx = np.arange(25, 75)
        image[idx[::-1], idx] = 255
        image[idx, idx] = 255

        # Classic straight-line Hough transform
        h, theta, d = hough_line(image)

        # Generating figure 1
        fig, axes = plt.subplots(1, 3, figsize=(15, 6),
                                 subplot_kw={'adjustable': 'box-forced'})
        ax = axes.ravel()

        ax[0].imshow(image, cmap=cm.gray)
        ax[0].set_title('Input image')
        ax[0].set_axis_off()

        ax[1].imshow(np.log(1 + h),
                     extent=[np.rad2deg(theta[-1]), np.rad2deg(theta[0]), d[-1], d[0]],
                     cmap=cm.gray, aspect=1/1.5)
        ax[1].set_title('Hough transform')
        ax[1].set_xlabel('Angles (degrees)')
        ax[1].set_ylabel('Distance (pixels)')
        ax[1].axis('image')

        ax[2].imshow(image, cmap=cm.gray)
        for _, angle, dist in zip(*hough_line_peaks(h, theta, d)):
            y0 = (dist - 0 * np.cos(angle)) / np.sin(angle)
            y1 = (dist - image.shape[1] * np.cos(angle)) / np.sin(angle)
            ax[2].plot((0, image.shape[1]), (y0, y1), '-r')
        ax[2].set_xlim((0, image.shape[1]))
        ax[2].set_ylim((image.shape[0], 0))
        ax[2].set_axis_off()
        ax[2].set_title('Detected lines')

        plt.tight_layout()
        plt.show()

        # Line finding using the Probabilistic Hough Transform
        image = data.camera()
        edges = canny(image, 2, 1, 25)
        lines = probabilistic_hough_line(edges, threshold=10, line_length=5,
                                         line_gap=3)

        # Generating figure 2
        fig, axes = plt.subplots(1, 3, figsize=(15, 5), sharex=True, sharey=True)
        ax = axes.ravel()

        ax[0].imshow(image, cmap=cm.gray)
        ax[0].set_title('Input image')

        ax[1].imshow(edges, cmap=cm.gray)
        ax[1].set_title('Canny edges')

        ax[2].imshow(edges * 0)
        for line in lines:
            p0, p1 = line
            ax[2].plot((p0[0], p1[0]), (p0[1], p1[1]))
        ax[2].set_xlim((0, image.shape[1]))
        ax[2].set_ylim((image.shape[0], 0))
        ax[2].set_title('Probabilistic Hough')

        for a in ax:
            a.set_axis_off()
            a.set_adjustable('box-forced')

        plt.tight_layout()
        plt.show()

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
test.addSection(0,0,1,1,"mathClass")
test.addSection(2,2,3,3,"class")
test.addSection(4,4,5,5,"mathClass")
processImage(test,"scheduletest.png")
# print(test.subSections)
