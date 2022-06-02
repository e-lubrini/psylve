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
import os
from tqdm import tqdm
from tools.utils import get_child_ext_path, try_read
from tools.eval_tools import word_is_correct_Q

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
import pikepdf

# pdfminer.six
from pdfminer.high_level import extract_text

# PyPDF4 txt + info
import PyPDF4

# TIKA
from tika import parser

# pdfreader
from pdfreader import SimplePDFViewer

# grobid
import requests

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
    for doc_object in tqdm(doc_objects, desc='pages processed by ocr', leave=False):
        extracted_text += (pytesseract.image_to_string(doc_object)+'\n')
    return extracted_text

def PyPDF4_ocr(pdf_filepath):
    doc_object = open(pdf_filepath, 'rb')
    reader = PyPDF4.PdfFileReader(pdf_filepath)
    if reader.isEncrypted:
        pdf = pikepdf.open(pdf_filepath, allow_overwriting_input=True)
        pdf.save(pdf_filepath)
    
    reader = PyPDF4.PdfFileReader(doc_object) # creating a pdf reader object
        
    n_pages = reader.numPages # #printing number of pages in pdf file
    text = ''

    for n in range(n_pages):
        pageObj = reader.getPage(n) # creating a page object
        text += pageObj.extractText() # extracting text from page
    return text

def pdfminer_ocr(pdf_filepath):
    return extract_text(pdf_filepath)

def tika_ocr(pdf_filepath):
    raw = parser.from_file(pdf_filepath)
    text = raw['content']
    return text
    
def pdfreader_extr(pdf_file_name):
    # get raw document
    with open(pdf_file_name, "rb") as f:
        fd = f.read()
    viewer = SimplePDFViewer(fd)

    metadata = viewer.metadata
    try:
        viewer.render()
        content = viewer.canvas.text_content
        return content
    except ValueError:
        #print('Value Error')
        return ''

def grobid_extr(pdf_filepath,
                grobid_inst_path,
                config_path,
                GROBID_URL,
                url,
                ):
    #subprocess.Popen(['bash','./gradlew run'], cwd=grobid_inst_path)
    xml = requests.put(url, files={'input': open(pdf_filepath, 'rb')})
    return xml.text


#############
### CONVS ###
#############

def get_txt(dir_path,
            tool_names,
            tools,
            storage_opts,
            overwrite_opts,
            ):
    extracted_txts = dict()
    for tool_name in tqdm(tool_names, desc='tools: ', leave=False):
        tool_txt_path = os.path.join(dir_path,tool_name,'ocr_extraction.txt')
        extracted_txts[tool_name] = try_read(tool_txt_path)
        extracted_txt_trans = False # TODO check if exists

        needs_txt = storage_opts['ocr_txt'] and (overwrite_opts['ocr_txt'] or not extracted_txts[tool_name])
        needs_txt_trans = storage_opts['ocr_txt_trans'] and (overwrite_opts['emb_txt_trans'] or not extracted_txts[tool_name])
        
        if needs_txt or needs_txt_trans:
            tool = tools[tool_name] 
            pdf_filepath = get_child_ext_path(dir_path, 'pdf')      # get path from doc # TODO: trat multiple pdfs per document
            extracted_txts[tool_name]= str(tool(pdf_filepath))  # pass it to tool
    return extracted_txts


def get_xml(dir_path,
            storage_opts,
            overwrite_opts,
            grobid_config,
            ):
    extracted_xml = try_read(dir_path, ext='.xml')
    extracted_xml_trans = False # TODO check if exists

    needs_xml = storage_opts['emb_xml'] and (overwrite_opts['emb_xml'] or not extracted_xml)
    needs_xml_trans = storage_opts['emb_txt_trans'] and (overwrite_opts['emb_txt_trans'] or not extracted_xml)
    
    if needs_xml or needs_xml_trans:
        pdf_filepath = get_child_ext_path(dir_path, 'pdf')
        extracted_xml = grobid_extr(pdf_filepath, **grobid_config)

    return extracted_xml