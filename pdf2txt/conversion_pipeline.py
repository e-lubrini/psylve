#!/bin/bash

#############
## IMPORTS ##
#############
import functools
import subprocess
import sys

from tools.utils import *
from tools.conv_tools import *
from tools import conv_tools as ctools

#############
## CONFIGS ##
#############
title_col = colors.blue
header_col = colors.cyan

input_dir_path = sys.argv[1]
if sys.argv[2]:
    verbose = True

##############
## PIPELINE ##
##############
mess_col('Conversion started!',title_col)

mess_col('Converting images to pdf documents...',header_col)
# if there are any imgs, convert them to pdf
not_pdf_filepaths = list_ext(input_dir_path,    # files to be converted to pdf
                            exts=['pdf'],
                            invert=True,
                            )
map(functools.partial(ctools.img2pdf,           # convert to pdf
                    input_dir_path_path=input_dir_path),
    not_pdf_filepaths)      

pdf_filepaths = list_ext(input_dir_path,        # all pdf files
                        exts=['pdf'],
                        invert=False,
                        )
mess_col('Rearranging folder structure...',header_col)
# rearrange folder structure
for pdf_filepath in pdf_filepaths:
    mv_to_custom_dir(pdf_filepath)

mess_col('Extracting text...',header_col)
# compile metadata for each file
for dir_path in tqdm(get_child_dir_paths(input_dir_path)):
    metadata = write_pdf_metadata(path=dir_path,
                                metadata_lab=['emb_txt',
                                            'lang_codes'],
                                )
# if file has embedded text, extract it with grobid
    if metadata['emb_txt']:
        #pdf2xml(dir_path, store_in_meta=True)
        pass

# convert file to text with ocr
    pdf2txt(dir_path,
            tool_names=['pytesseract_ocr'],
            tools=get_funs_from_module(ctools),
            save_in_dir=True,
            overwrite=True,
            )

# translate text to English
mess_col('Translating documents...',header_col)
for dir_path in tqdm(get_child_dir_paths(input_dir_path)):
    translate_doc(dir_path)

mess_col('Conversion successful!',title_col)