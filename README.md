# Uniform-Image-Processing-Library
A Python library which facilitates the processing of images with a uniform layout (e.g. calendars, schedules, etc.) and inputting their data into a csv data file.

Dependencies:
You will need to import the Python Image Library (PIL), Tesseract, PyTesseract, and CSV.
It's a little complicated to install Tesseract and PyTesseract on Macs, but here's a very simple and easy to follow guide (it only involves a few command line prompts): http://benschmidt.org/dighist13/?page_id=129

Current Status:
Currently, I've created a blueprint object which holds all the subdivisions and their coordinates (called subsections) of the uniform image. I've also created a function which takes in the blueprint and an image file, which then processes the contents of each subsection and inputs them into a csv file (unfinished).

Possible Changes:
- Feel free to add different functionalities to either the blueprint object or the processing function.
  - Possibly, add the ability to define which subsections correspond to headers and which correspond to the headers data.
  - Add a section which processes the color of the subsection and does something accordingly
  - Test if handwritten files work
