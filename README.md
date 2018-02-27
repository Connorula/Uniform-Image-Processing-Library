# Uniform-Image-Processing-Library
A Python library which facilitates the processing of numerous images with a uniform layout (e.g. calendars, schedules, etc.) by inputting their textual data into a CSV file.

## In-Depth Explanation
Essentially, the user creates a uImageBlueprint object, which serves as the base template for all the image processing. The object contains the individual sections of the image which the user wishes to process and input into a data file. These sections are contained within a dictionary, where the keys represent the header and the values are the coordinates of the section whose text will correspond to the header in the CSV file. The user can define the bounds of the sections in a variety of ways. The user can manually add sections to the blueprint by using the addSection function. However, this requires knowing the approximate pixel coordinates of the each section's top-left and bottom-right coordinate (one can determine a pixel's location by using software such as Gimp). Alternatively, the user can use the findSections function, which will automatically segment the image into rectangles according to the threshold value (color of the line dividing each segment) and minimum segment area (the approximate minimum size of each section). If necessary, the user can iron out the issues with the automatically processed image by removing/adding sections which were not recognized by the automated function. Once the user has a satisfying blueprint object, they can proceed to process either a single image or a folder full of images by using the processImage and processFolder functions, respectively. When the user calls these functions, the text within each section will be read, and inputted into a CSV file whose headers are the section dictionary's keys.

## Dependencies:
You will need to import the Python Image Library (PIL), Tesseract, PyTesseract, OpenCV, Numpy, and Pathlib.
It's a little complicated to install Tesseract on Macs, but here's a very simple and easy to follow guide (it only involves a few command line prompts): http://benschmidt.org/dighist13/?page_id=129

## Current Status:
Currently, I've created a blueprint object which holds all the subdivisions and their coordinates (called subsections) of the uniform image. I've also created a function which takes in the blueprint and an image file, which then processes the contents of each subsection and inputs them into a csv file (unfinished).

## Possible Changes:
- Feel free to add different functionalities to either the blueprint object or the processing function.
  - Possibly, add the ability to define which subsections correspond to headers and which correspond to the headers data.
  - Add a section which processes the color of the subsection and does something accordingly
  - Test if handwritten files work
  - Or, come up with anything you think would be useful (different outputs, added functionality, etc.) This project is still in its early stages, so don't be afraid to contribute something drastically different!
