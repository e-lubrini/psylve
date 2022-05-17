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
from tools.utils import *

# pdf<>png
import os
import fitz
from PIL import Image
from fpdf import FPDF

# pytesseract
import pytesseract
import os
from PIL import Image

# PyPDF4
import PyPDF4

# pdfminer.six
from pdfminer.high_level import extract_text

# PyPDF4 txt + info
import PyPDF4

# TIKA
from tika import parser

# pdfreader
from pdfreader import SimplePDFViewer

# grobid
from tools.grobid import grobid

#############
### TOOLS ###
#############

named_conversion_tools = dict()
ext_name_tool = dict()

## Functions taking a list of objects as first argument
## TODO Class to specify source/target extension
##print('Tools converting in the following extensions:')

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
#print(pdf2img.extensions)

def img2pdf(paths):
    pdf = FPDF()
    for path in paths:
        pdf.add_page()
        try:
            pdf.image(path)
        except:
            print(path)
            print('Warning: "{0}" extension not supported for conversion to pdf'.format(path[:-4]))
    pdf.output(path[:-4]+'.pdf', "F")

img2pdf.extensions = ('[img]', 'pdf')
#print(img2pdf.extensions)

## >txt

def pytesseract_ocr(pdf_filepath):
    doc_objects = pdf2img(pdf_filepath)
    extracted_text = ''
    for doc_object in doc_objects:
        extracted_text += (pytesseract.image_to_string(doc_object)+'\n')
    return extracted_text

pytesseract_ocr.extensions = ('png', 'txt')
#print(pytesseract_ocr.extensions)


def PyPDF4_ocr(pdf_filepath):
    doc_object = open(pdf_filepath, 'rb')

    pdfReader = PyPDF4.PdfFileReader(doc_object) # creating a pdf reader object
    
    n_pages = pdfReader.numPages # #printing number of pages in pdf file
    text = ''

    for n in range(n_pages):
        pageObj = pdfReader.getPage(n) # creating a page object
        text += pageObj.extractText() # extracting text from page
    return text

PyPDF4_ocr.extensions = ('pdf', 'txt')
#print(PyPDF4_ocr.extensions)


def pdfminer_ocr(pdf_filepath):
    return extract_text(pdf_filepath)

pdfminer_ocr.extensions = ('pdf', 'txt')
#print(pdfminer_ocr.extensions)

def tika_ocr(pdf_filepath):
    raw = parser.from_file(pdf_filepath)
    text = raw['content']
    return text
    
tika_ocr.extensions = ('pdf', 'txt')
#print(tika_ocr.extensions)

def pdfreader_ocr(pdf_file_name):
    # get raw document
    fd = open(pdf_file_name, "rb")
    viewer = SimplePDFViewer(fd)
    metadata = viewer.metadata
    try:
        viewer.render()
        content = viewer.canvas.text_content
        return content
    except ValueError:
        #print('Value Error')
        return ''

pdfreader_ocr.extensions = ('pdf', 'txt')
#print(pdfreader_ocr.extensions)


def grobid_extr(pdf_filepath):
    return grobid.extract_emb_txt(pdf_filepath)

grobid_extr.extensions = ('pdf', 'txt')
#print(grobid_extr.extensions)

def pdf2txt(doc_dir_path,
            tool_names,
            tools,
            overwrite=False,
            ):
    extracted_texts = dict()
    for tool_name in tool_names:
        output_dir_path = os.path.join(doc_dir_path,tool_name)
        if not os.path.exists(output_dir_path):
            os.mkdir(output_dir_path)
        tool = tools[tool_name]
        pdf_filepath = get_child_ext_path(doc_dir_path, 'pdf')      # get path from doc # TODO: trat multiple pdfs per document
        dbg(tool)
        dbg(pdf_filepath[-5:])
        extracted_texts[tool_name]= tool(pdf_filepath)  # pass it to tool
        output_filepath = os.path.join(output_dir_path,tool_name+'.txt')
        if overwrite==True or not os.path.exists(output_filepath):
            with open(output_filepath, 'w+') as f:
                    f.write(extracted_texts[tool_name])
    return extracted_texts

def pdf2xml(dir_path):
    pdf_filepath = get_child_ext_path(dir_path, 'pdf')
    extracted_xml = grobid_extr(pdf_filepath)
    output_dir_path = os.path.join(dir_path,'grobid')
    os.mkdir(output_filpath)
    output_filpath = os.path.join(output_dir_path,'grobid.txt')
    with open(output_filpath, 'w') as f:
            f.write(extracted_xml)