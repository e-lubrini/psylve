#########################################################################################
# this file
# (1) imports tools for conversion,
# (2) defines functions using such tools
# (for standardisation, so that they take the same arguments and return the same output),
# and (3) store relevant info about the funtions in a dictionary
#########################################################################################

#############
## IMPORTS ##
#############

from distutils import extension
import os
from matplotlib import image

# pdf<>png
import os
import fitz
from PIL import Image

# pytesseract
import pytesseract
import shutil
import os
import random
#try:
from PIL import Image
#except ImportError:
#import Image

# PyPDF4
import PyPDF4

# pdfminer.six
import pdfminer
from pdfminer.high_level import extract_text

# PyPDF4 txt + info
import PyPDF4
from PyPDF4 import PdfFileReader

# TIKA
from tika import parser


#############
### TOOLS ###
#############


## Functions taking a list of objects as first argument
## TODO Class to specify source/target extension
print('Tools converting in the following extensions:')

## pdf<>png
def pdf2img(doc_objects):
    
    compression = 'zip' # either "zip", "lzw", "group4"

    zoom = 2 # to increase the resolution
    mat = fitz.Matrix(zoom, zoom)
    image_list = []

    for doc_object in doc_objects:   
        for page in doc_object:
            pix = page.get_pixmap(matrix = mat)
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            image_list.append(img)
    return image_list

pdf2img.extensions = ('pdf', 'png')
print(pdf2img.extensions)

## >txt

def pytesseract_ocr(doc_objects):
    for doc_object in doc_objects:
        extracted_text = ''
        extracted_text += (pytesseract.image_to_string(doc_object)+'\n')
    return extracted_text

pytesseract_ocr.extensions = ('png', 'txt')
print(pytesseract_ocr.extensions)


def PyPDF4_ocr(doc_object):
    
    pdfReader = PyPDF4.PdfFileReader(doc_object) # creating a pdf reader object
    
    print(pdfReader.numPages) # printing number of pages in pdf file
    
    pageObj = pdfReader.getPage(0) # creating a page object
    
    text = pageObj.extractText() # extracting text from page
    return text

PyPDF4_ocr.extensions = ('pdf', 'txt')
print(PyPDF4_ocr.extensions)

#####################
### DICT OF TOOLS ###
#####################

local_functions = dict(locals())

named_conversion_tools = dict()
for key, value in local_functions.items():
    if "function" in str(value) and 'builtins' not in str(key):
        #print(locals()[key])
        named_conversion_tools[key] = locals()[key]

ext_name_tool = dict()
for name, tool in named_conversion_tools.items():
    
    print('Tools available:')
    try:
        ext = tool.extensions
        ext_name_tool[ext] = dict()
        ext_name_tool[ext][name]=tool
    except AttributeError:
        continue
    

tools = ext_name_tool

#####################################
### DICT OF TOOL EXT REQUIREMENTS ###
#####################################

tool_ext_req = dict()

for (input_ext,_),tooldict in tools.items():
    for tool_name in tooldict.keys():
        tool_ext_req[tool_name] = input_ext

ter = tool_ext_req
