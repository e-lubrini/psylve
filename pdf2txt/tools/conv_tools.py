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

## >txt

def pytesseract_ocr(pdf_filepath):
    doc_objects = pdf2img(pdf_filepath)
    extracted_text = ''
    for doc_object in doc_objects:
        extracted_text += (pytesseract.image_to_string(doc_object)+'\n')
    return extracted_text

def PyPDF4_ocr(pdf_filepath):
    doc_object = open(pdf_filepath, 'rb')

    pdfReader = PyPDF4.PdfFileReader(doc_object) # creating a pdf reader object
    
    n_pages = pdfReader.numPages # #printing number of pages in pdf file
    text = ''

    for n in range(n_pages):
        pageObj = pdfReader.getPage(n) # creating a page object
        text += pageObj.extractText() # extracting text from page
    return text

def pdfminer_ocr(pdf_filepath):
    return extract_text(pdf_filepath)

def tika_ocr(pdf_filepath):
    raw = parser.from_file(pdf_filepath)
    text = raw['content']
    return text
    
def pdfreader_ocr(pdf_file_name):
    # get raw document
    with open(pdf_file_name, "rb") as f:
        fd = f.read()
    dbg(fd[-10:])
    viewer = SimplePDFViewer(fd)

    metadata = viewer.metadata
    try:
        viewer.render()
        content = viewer.canvas.text_content
        return content
    except ValueError:
        #print('Value Error')
        return ''

def grobid_extr(pdf_filepath):
    return grobid.extract_emb_txt(pdf_filepath)


#############
### CONVS ###
#############

def pdf2txt(doc_dir_path,
            tool_names,
            tools,
            save_in_dir=True,
            overwrite=False,
            ):
    extracted_texts = dict()
    for tool_name in tool_names:
        output_dir_path = os.path.join(doc_dir_path,tool_name)
        if not os.path.exists(output_dir_path):
            os.mkdir(output_dir_path)
        tool = tools[tool_name]
        pdf_filepath = get_child_ext_path(doc_dir_path, 'pdf')      # get path from doc # TODO: trat multiple pdfs per document
        extracted_texts[tool_name]= str(tool(pdf_filepath))  # pass it to tool
        output_filepath = os.path.join(output_dir_path,tool_name+'.txt')
        if save_in_dir==True and (overwrite==True or not os.path.exists(output_filepath)):
            with open(output_filepath, 'w+') as f:
                    f.write(extracted_texts[tool_name])
    return extracted_texts

def pdf2xml(dir_path,
            save_in_dir=False,
            overwrite=True,):
    pdf_filepath = get_child_ext_path(dir_path, 'pdf')
    extracted_xml = grobid_extr(pdf_filepath)
    output_dir_path = os.path.join(dir_path,'grobid')
    os.mkdir(output_filepath)
    output_filepath = os.path.join(output_dir_path,'grobid.txt')
    if save_in_dir==True and (overwrite==True or not os.path.exists(output_filepath)):
        with open(output_filepath, 'w') as f:
            f.write(extracted_xml)