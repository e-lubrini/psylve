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
try:
 from PIL import Image
except ImportError:
 import Image

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
## ALWAYS specify source/target extension!!!

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

pdf2img.extensions =(pdf, img)


## >txt

def pytesseract_ocr(doc_objects):
    for doc_object in doc_objects:
        extracted_text = ''
        extracted_text += (pytesseract.image_to_string(doc_object)+'\n')
    return extracted_text


#####################
### DICT OF TOOLS ###
#####################

named_conversion_tools = dict()
for key, value in locals().items():
    if callable(value) and value.__module__ == __name__:
        named_conversion_tools[key] = locals()[key]

ext_name_tool = dict()
for name, tool in named_conversion_tools.items():
    ext_name_tool[tool.extensions] = dict()
    ext_name_tool[tool.extensions][name]=tool

tools = ext_name_tool