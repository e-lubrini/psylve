#!/bin/bash

#############
## IMPORTS ##
#############
import functools
import sys

from tools.utils import colours
from tools.utils import *
from tools.conv_tools import *
from tools import conv_tools as ctools

#############
## CONFIGS ##
#############
# open configuration file from path
config_file_path = sys.argv[1]
with open(config_file_path, 'r') as f:
    configs = json.load(f)

# colours
mess_cols = configs['appearance']['message_colours']
col_config = dict(title_col = colours[mess_cols['start']],
                    header_col = colours[mess_cols['stages']],
                    end_col = colours[mess_cols['end']],
                    )

# verbose
try:
    sys.argv[2]
    verbose = colours[mess_cols['verbose']]
except IndexError:
    verbose = False

# general
input_dir_path = configs['dataset']['path']
conv_tool_names = configs['conversion']['tool_names']

# metadata
overwrite_metadata_keys = []
for k,v in configs['general']['overwrite']:
    overwrite_metadata_keys.append(k) if v else None

# grobid
grobid_configs = configs['grobid']
grobid_config = dict(grobid_inst_path=['grobid_inst_path'],
                    config_path=grobid_configs['config_path'],
                    GROBID_URL=grobid_configs['GROBID_URL'],
                    url=grobid_configs['GROBID_URL']+configs['grobid']['end_url'],
                    )

##############
## PIPELINE ##
##############
mess_col('Conversion started!',col_config.title_col)

mess_col('Converting images to pdf documents...',col_config.header_col)
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
mess_col('Rearranging folder structure...',col_config.header_col)
# rearrange folder structure
for pdf_filepath in pdf_filepaths:
    mv_to_custom_dir(pdf_filepath)

mess_col('Extracting text...',col_config.header_col)
# compile metadata for each file
for dir_path in tqdm(get_child_dir_paths(input_dir_path)):
    verbose_mess('Processing: '+dir_path, verbose)
    metadata = write_pdf_metadata(path=dir_path,
                                overwrite_keys=overwrite_metadata_keys,
                                )

# if file has embedded text, extract it with grobid
    if metadata['emb_txt'] and '' not in metadata.keys():
        pdf2xml(dir_path=dir_path,
                grobid_config=grobid_config,
                store_in_meta=True,
                save_in_dir=False,
                overwrite=True,
                )

# convert file to text with ocr
    pdf2txt(dir_path,
            tool_names=conv_tool_names,
            tools=get_funs_from_module(ctools),
            save_in_dir=True,
            overwrite=True,
            )

# translate text to English
mess_col('Translating documents...',col_config.header_col)
for dir_path in tqdm(get_child_dir_paths(input_dir_path)):
    verbose_mess('Processing: '+dir_path, verbose)
    translate_doc(dir_path)

mess_col('Conversion successful!',col_config.title_col)