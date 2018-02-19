from PIL import Image
from pytesseract import image_to_string
import csv
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

# test = uImageBlueprint("Connor","png")
# test.addSection(0,0,1,1,"mathClass")
# test.addSection(2,2,3,3,"class")
# test.addSection(4,4,5,5,"mathClass")
# processImage(test,"scheduletest.png")
# print(test.subSections)
