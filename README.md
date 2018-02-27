# Uniform-Image-Processing-Library
A Python library which facilitates the processing of numerous images with a uniform layout (e.g. calendars, schedules, etc.) by inputting their textual data into a CSV file.

## In-Depth Explanation
Essentially, the user creates a uImageBlueprint object, which serves as the base template for all the image processing. The object contains the individual sections of the image which the user wishes to process and input into a data file. These sections are contained within a dictionary, where the keys represent the headers of the CSV and the values are the coordinates of the section whose text will correspond to the appropriate CSV header. The user can define the bounds of the sections in a variety of ways. The user can manually add sections to the blueprint by using the addSection function. However, this requires knowing the approximate pixel coordinates of the each section's top-left and bottom-right coordinate (one can determine a pixel's location by using software such as Gimp). Alternatively, the user can use the findSections function, which will automatically segment the image into rectangles according to the threshold value (color of the line dividing each segment) and minimum segment area (the approximate minimum size of each section). If necessary, the user can iron out the issues with the automatically processed image by removing/adding sections which were not recognized by the automated function. Once the user has a satisfying blueprint object, they can proceed to process either a single image or a folder full of images by using the processImage and processFolder functions, respectively. When the user calls these functions, the text within each section will be read, and inputted into a CSV file whose headers are the section dictionary's keys.

## Dependencies:
You will need to import the following libraries: Pillow, Matplotlib, Tesseract, PyTesseract, OpenCV, Numpy, and Pathlib.
```
pip install pillow
pip install pytesseract
pip install numpy
pip install matplotlib
pip install pathlib
pip install opencv-python
```
It's a little complicated to install Tesseract on Macs, but [here's](http://benschmidt.org/dighist13/?page_id=129) a very simple and easy-to-follow guide (only go up to `brew install tesseract` in Step 3).

## Documentation
### `addSection(self, coordinates, name)`
The addSection function adds a subsection with specified coordinates to the subsection dictionary under either a preexisting key or a new one.
* coordinates: This parameter requires a list with 4 integers, where the first and second integers correspond to the coordinates - (x1,y1) - of the subsection's top-left corner and the third and fourth integers correspond to the coordinates - (x2,y2) - of the subsection's bottom-right corner. If x1 > x2 or y1>y2, the function will throw print "Invalid coordinates" to the console.
* name: This parameter requires a string. If the key name already exists in the subSections dictionary, the section's coordinates will be appended to the key's array of coordinates.
#### Example
```
test = uImageBlueprint("PASchedule","png")
test.addSection([0,0,1,1],"bio")
test.addSection([1,1,2,2],"bio")
test.addSection([500,2271,989,2578],"comp sci")
test.addSection([0,1325,495,1650],"mathClass")
print(test.subSections)
```
This returns:
```
{'bio': [[0, 0, 1, 1], [1, 1, 2, 2]], 'comp sci': [[500, 2271, 989, 2578]], 'mathClass': [[0, 1325, 495, 1650]]}
```

### `removeSection(self, headerName, index)`
The removeSection function removes a subsection/many subsections from the uImageBlueprint's subSection dictionary.
* headerName: This parameter requires a list containing the key values of the sections the user wishes to remove.
* index: This parameter requires a list containing the indices of the subsections the user wishes to remove. If the list only contains -1, all the sections of the specified header(s) will be removed. If the indices are out of range for a particular header, nothing will occur.
#### Example
```
test = uImageBlueprint("PASchedule","png")
test.addSection([0,0,1,1],"bio")
test.addSection([1,1,2,2],"bio")
test.addSection([500,2271,989,2578],"comp sci")
test.addSection([0,1325,495,1650],"mathClass")
test.removeSection(["bio","mathClass"],[1])
print("First Deletion: " + str(test.subSections))
test.removeSection(["bio","mathClass"],[-1])
print("Second Deletion: " + str(test.subSections))
```
This returns:
```
First Deletion: {'bio': [[0, 0, 1, 1]], 'comp sci': [[500, 2271, 989, 2578]], 'mathClass': [[0, 1325, 495, 1650]]}
Second Deletion: {'comp sci': [[500, 2271, 989, 2578]]}
```

### `renameSection(self, headerName, newHeaderName, index)`
The renameSection function renames an entire section or a particular coordinate of a section.
* headerName: This parameter requires a string which corresponds to a key of the subSections dictionary.
* newHeaderName: This parameter requires a string, and, if it is not a preexisting key, will create a new key value and store the appropriate values key within it. If the key already exists, it will simply append the appropriate values to the end of the key's list of coordinates.
* index: This parameter takes in an integer. If the integer is -1, the entirety of the subSection under headerName will be renamed to newHeaderName. If an index is specified, the coordinate at position index of the list of coordinates of the headerName key will be renamed to newHeaderName.
#### Example
```
test = uImageBlueprint("PASchedule","png")
test.addSection([0,0,1,1],"bio")
test.addSection([1,1,2,2],"bio")
test.addSection([500,2271,989,2578],"comp sci")
test.addSection([0,1325,495,1650],"mathClass")
test.renameSection("bio","comp sci", -1)
print(test.subSections)
test.renameSection("comp sci", "bio", 1)
print(test.subSections)
```
This prints the following to the console:
```
{'comp sci': [[500, 2271, 989, 2578], [0, 0, 1, 1], [1, 1, 2, 2]], 'mathClass': [[0, 1325, 495, 1650]]}
{'comp sci': [[500, 2271, 989, 2578], [1, 1, 2, 2]], 'mathClass': [[0, 1325, 495, 1650]], 'bio': [[0, 0, 1, 1]]}
```

### `getSectionText(self, headerName, fileName, index)`
This function returns the text within a particular section of the image.
* headerName: This parameter requires a string which corresponds to a key of the subSections dictionary.
* fileName: Name of the file you wish to read the text from. Note that if the file is not in the current directory, you must add the path to the fileName.
* index: This parameter requires an integer. This parameter specifies which element of the coordinate list stored in the subSections dictionary under headerNamer you wish to retrieve the text from.
#### Example
```
test = uImageBlueprint("PASchedule","png")
test.addSection([0,0,1,1],"bio")
test.addSection([1,1,2,2],"bio")
test.addSection([500,2271,989,2578],"comp sci")
test.addSection([0,1325,495,1650],"mathClass")
print(test.getSectionText("comp sci", "scheduletest.png",0))
```
This prints the following to the console:
```
2:00 - 2:45
CSCG30
N. Zufelt
MORSEHL-103
```

### `findSections(self,fileName,threshold,boxArea)`
This function automatically finds the sections of an image, and adds them to the subSections dictionary of the uImageBlueprint object.
* fileName: This parameter requires the fileName you wish to segment into sections. Note that if the file is not in the current directory, you must add the path to the fileName.
* threshold: This parameter requires an integer, and determines which lines are considered contours.
* boxArea: This parameter also requires an integer which is an approximation of the minimum section size, in order to filter out non-sectional data.
Note that the threshold and boxArea will vary from blueprint to blueprint. In order to facilitate the finding of the correct threshold and boxArea, the function creates an image called *test.png* which shows the contours in green, the top-left coordinate of the box as a red circle, the bottom-right coordinate of the box as a blue circle, and the section name of said box in red in the middle. I recommend you start at a boxArea of 0, so nothing gets filtered out, and adjust the threshold until you find a satisfactory value. From there, you can adjust the boxArea to filter out any unwanted sections. If all else fails, manually remove/add sections using the appropriate functions until you've reached the blueprint which you desire.
#### Example
```
test = uImageBlueprint("PASchedule","png")
test.findSections("scheduletest.png",127,30000)
print(test.subSections)
```
This prints the following:
```
{0: [[1984, 2584, 2473, 2895]], 1: [[500, 2584, 988, 2895]], 2: [[5, 2584, 494, 2895]], 3: [[1983, 2271, 2474, 2578]], 4: [[1489, 2271, 1978, 2579]], 5: [[994, 2272, 1484, 2895]], 6: [[500, 2271, 989, 2578]], 7: [[4, 2271, 495, 2578]], 8: [[1983, 1958, 2474, 2266]], 9: [[1489, 1958, 1978, 2266]], 10: [[994, 1958, 1484, 2266]], 11: [[500, 1958, 989, 2266]], 12: [[4, 1959, 495, 2265]], 13: [[1983, 1646, 2474, 1953]], 14: [[1489, 1646, 1978, 1953]], 15: [[993, 1647, 1485, 1952]], 16: [[500, 1646, 989, 1954]], 17: [[4, 1646, 495, 1953]], 18: [[1983, 1333, 2474, 1641]], 19: [[1489, 1333, 1978, 1641]], 20: [[993, 1333, 1485, 1641]], 21: [[500, 1333, 989, 1641]], 22: [[4, 1333, 495, 1641]], 23: [[1983, 1021, 2474, 1328]], 24: [[993, 1021, 1485, 1329]], 25: [[500, 1021, 988, 1328]], 26: [[4, 1021, 495, 1328]], 27: [[1489, 1021, 1979, 1328]], 28: [[1490, 709, 1978, 1016]], 29: [[1983, 708, 2474, 1016]], 30: [[993, 708, 1485, 1016]], 31: [[499, 709, 989, 1016]], 32: [[4, 708, 495, 1016]], 33: [[1983, 396, 2474, 704]], 34: [[1490, 396, 1978, 703]], 35: [[500, 396, 989, 704]], 36: [[4, 396, 495, 704]], 37: [[1983, 83, 2474, 391]], 38: [[1489, 83, 1979, 390]], 39: [[993, 84, 1485, 390]], 40: [[500, 83, 989, 391]], 41: [[4, 83, 495, 391]], 42: [[1984, 5, 2474, 77]], 43: [[1491, 4, 1978, 77]], 44: [[995, 4, 1484, 78]], 45: [[501, 4, 988, 78]], 46: [[4, 5, 494, 78]]}
```

### `processImage(self,imageFile,csvFile)`
This function processes a single image using the corresponding uImageBlueprint, and stores the textual data of each section in a CSV file.
* imageFile: This parameter requires the name of the image file you wish to process. If the file does not exist within the current directory, pass the file path instead.
* csvFile: This parameter requires the name of the CSV file you wish to add the data to. If the CSV file already exists in the current directory, the data will be appended to the preexisting CSV's end. Otherwise, a new CSV file will be created under the parameter's name.
#### Example
```
test = uImageBlueprint("PASchedule","png")
test.findSections("scheduletest.png",127,30000)
test.processImage("scheduletest.png","text.csv")
```
This will write all the textual data within the sections of test of scheduletest.png into a CSV called *text.csv*.

### `processFolder(self,csvFile, path)`
This function processes a folder of images using the corresponding uImageBlueprint, and stores all of their textual data into a CSV file.
* csvFile: This parameter requires the name of the CSV file you wish to add the data to. If the CSV file already exists in the current directory, the data will be appended to the preexisting CSV's end. Otherwise, a new CSV file will be created under the parameter's name.
* path: This parameter requires the path, relative to the current directory, of the folder containing the images. If the images are contained within the current directory, pass a blank string for path.
#### Example
```
test = uImageBlueprint("PASchedule","png")
test.addSection([500,2271,989,2578],"comp sci")
test.addSection([0,1325,495,1650],"mathClass")
test.processFolder("newCSV.csv", "/images")
```
This will process all the images in ./images according to the test uImageBlueprint, and store the textual data into a CSV file called newCSV.csv.

## FAQs
- findSections is not working for my image!

You're going to want to do a couple things to maximize the performance of the findSections and processImage/processFolder functions. Firstly, you'll want to use images with a DPI of at least 300. There are many ways to achieve this, and tutorials can be found online. Furthermore, you'll want to crop your image to fit as closely around the image's border as possible, as to limit the surrounding white space. Lastly, you must understand that it is not a perfect function, and will oftentimes require manual addition/removal of sections to achieve a satisfactory result.

## Possible Changes:
Feel free to add different functionalities to either the blueprint object or the processing function.
- [ ] Add the ability to define which subsections correspond to headers and which correspond to the headers data.
- [ ] Add a section which returns the dominant color of the subsection
- [ ] Test if handwritten files work
- [ ] Improve contour recognition of findSections function
- [ ] Add ability to have sections that aren't just rectangles
- [ ] Function which returns list of intersections of contours, so user can more easily add/remove sections.
- [ ] Or, come up with anything you think would be useful (different outputs, added functionality, etc.) This project is still in its early stages, so don't be afraid to contribute something drastically different!

## License
This project is licensed under the MIT License - see the LICENSE.md file for details

## Authors
Connor Devlin - cdevlin@andover.edu
