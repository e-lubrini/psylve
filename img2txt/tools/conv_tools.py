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
from fpdf import FPDF

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

# pdfreader
from pdfreader import PDFDocument, SimplePDFViewer


#############
### TOOLS ###
#############

named_conversion_tools = dict()
ext_name_tool = dict()

## Functions taking a list of objects as first argument
## TODO Class to specify source/target extension
print('Tools converting in the following extensions:')

## pdf<>png
def pdf2img(pdf_filepath):
    
    compression = 'zip' # either "zip", "lzw", "group4"

    zoom = 2 # to increase the resolution
    mat = fitz.Matrix(zoom, zoom)
    doc = fitz.open(pdf_filepath)
    image_list = []
  
    for page in doc:
        pix = page.get_pixmap(matrix = mat)
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        image_list.append(img)
    return image_list

pdf2img.extensions = ('pdf', 'png')
ext_name_tool[('pdf', 'png')] = {}
print(pdf2img.extensions)

def img2pdf(img_filepaths):
    pdf = FPDF()
    for img_filepath in img_filepaths:
        pdf.add_page()
        pdf.image(img_filepath)
    pdf.output(os.path.split(img_filepath)[-2], "F")

img2pdf.extensions = ('[img]', 'pdf')
ext_name_tool[('[img]', 'pdf')] = {}
print(img2pdf.extensions)

## >txt

def pytesseract_ocr(pdf_filepath):
    doc_objects = pdf2img(pdf_filepath)
    extracted_text = ''
    for doc_object in doc_objects:
        extracted_text += (pytesseract.image_to_string(doc_object)+'\n')
    return extracted_text

pytesseract_ocr.extensions = ('png', 'txt')
ext_name_tool[('png', 'txt')] = {}
print(pytesseract_ocr.extensions)


def PyPDF4_ocr(pdf_filepath):
    doc_object = open(pdf_filepath, 'rb')

    pdfReader = PyPDF4.PdfFileReader(doc_object) # creating a pdf reader object
    
    n_pages = pdfReader.numPages # printing number of pages in pdf file
    text = ''

    for n in range(n_pages):
        pageObj = pdfReader.getPage(n) # creating a page object
        text += pageObj.extractText() # extracting text from page
    return text

PyPDF4_ocr.extensions = ('pdf', 'txt')
ext_name_tool[('pdf', 'txt')] = {}
print(PyPDF4_ocr.extensions)


def pdfminer_ocr(pdf_filepath):
    return extract_text(pdf_filepath)

pdfminer_ocr.extensions = ('pdf', 'txt')
ext_name_tool[('pdf', 'txt')] = {}
print(pdfminer_ocr.extensions)

def tika_ocr(pdf_filepath):
    raw = parser.from_file(pdf_filepath)
    text = raw['content']
    return text
    
tika_ocr.extensions = ('pdf', 'txt')
ext_name_tool[('pdf', 'txt')] = {}
print(tika_ocr.extensions)

def pdfreader_ocr(pdf_file_name):
    # get raw document
    fd = open(pdf_file_name, "rb")
    viewer = SimplePDFViewer(fd)
    metadata = viewer.metadata
    try:
        viewer.render()
        content = viewer.canvas.text_content
    except ValueError:
        print('Value Error')
    return content

pdfreader_ocr.extensions = ('pdf', 'txt')
ext_name_tool[('pdf', 'txt')] = {}
print(pdfreader_ocr.extensions)

##########################
### CONV AND SAVE TOOL ###
##########################

def conv_ad_save(dir_path,
                doc_object,
                converter,
                tool_names,
                overwrite = False,
                OKCYAN = '\033[96m',
                ENDC = '\033[0m'):
    print(OKCYAN + 'Converting:', dir_path + ENDC)
      
    # convert to jpg/pdf
    doc_object.to_target_format('png')
    doc_object.to_target_format('pdf')
    print(doc_object.data['pdf'])
    
    # convert to txt with all tools
    converter.convert_to_txt(doc_object, tool_names=tool_names)
    
    # save all
    doc_object.save_all_txt_conversions(dir_path, overwrite)
    return

#####################
### DICT OF TOOLS ###
#####################

named_conversion_tools = {}
local_functions = dict(locals())

for key, value in local_functions.items():
    if "function" in str(value) and 'builtins' not in str(key):
        #print(locals()[key])
        named_conversion_tools[key] = locals()[key]


logs = []

for name, tool in named_conversion_tools.items():
    try:
        ext = tool.extensions
        ext_name_tool[ext][name]=tool
        logs.append([ext,ext_name_tool])
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
