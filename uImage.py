from PIL import Image
from pytesseract import image_to_string

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




test = uImageBlueprint("Connor","png")
test.addSection(0,0,1,1,"mathClass")
test.addSection(2,2,3,3,"class")
test.addSection(4,4,5,5,"newClass")
print(test.subSections)
