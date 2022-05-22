#!/bin/bash

#############
## IMPORTS ##
#############
import functools
import sys

from executing import Source

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

mess_col('Loading onfigurations...',col_config['title_col'])

# verbose
try:
    sys.argv[2]
    verbose = colours[mess_cols['verbose']]
except IndexError:
    verbose = False
dbg(bool(verbose))

# general
input_dir_path = configs['dataset']['path']
dbg(input_dir_path)
conv_tool_names = configs['conversion']['tool_names']
dbg(conv_tool_names)

# storage
storage_keys = configs['general']['store_output']
dbg(storage_keys)

# overwrite
overwrite_keys = configs['general']['overwrite']
dbg(overwrite_keys)

# grobid
grobid_configs = configs['grobid']
grobid_config = dict(grobid_inst_path=grobid_configs['grobid_inst_path'],
                    config_path=grobid_configs['config_path'],
                    GROBID_URL=grobid_configs['GROBID_URL'],
                    url=grobid_configs['GROBID_URL']+configs['grobid']['end_url'],
                    )
dbg(grobid_config['grobid_inst_path'])

##############
## PIPELINE ##
##############
mess_col('Conversion started!',col_config['title_col'])

## CONVERT IMAGES TO PDFS
mess_col('Converting images to pdf documents...',col_config['header_col'])
not_pdf_filepaths = list_ext(input_dir_path,    # files to be converted to pdf
                            exts=['pdf'],
                            invert=True,
                            )
map(functools.partial(ctools.img2pdf,           # convert to pdf
                    input_dir_path_path=input_dir_path),
    not_pdf_filepaths)      


## REARRANGE FOLDER STRUCTURE
mess_col('Rearranging folder structure...',col_config['header_col'])
pdf_filepaths = list_ext(input_dir_path,
                        exts=['pdf'],
                        invert=False,
                        )
for pdf_filepath in pdf_filepaths:
    mv_to_custom_dir(pdf_filepath)


## START EXTRACTING DATA
mess_col('Extracting text...',col_config['header_col'])
for dir_path in tqdm(get_child_dir_paths(input_dir_path)):
    verbose_mess('Processing: '+dir_path, verbose)

# compile metadata for each file
    # TODO verbose need metadata, etc.
    metadata = get_metadata(dir_path,
                            storage_opts=storage_keys,
                            overwrite_opts=overwrite_keys,
                            )

    store_data(storage='meta',
                data=metadata,
                dir_path=dir_path,
                name='metadata',
                )

# extract embedded xml and translate to English
    emb_xml = get_xml(dir_path,
                storage_opts=storage_keys,
                overwrite_opts=overwrite_keys,
                grobid_config=grobid_config,
                )

    store_data(storage='dir',
                data=emb_xml,
                dir_path=dir_path,
                name='grobid',
                )

    emb_xml_trans = get_translation(tool_dir_path=os.path.join(dir_path,'grobid'),
                            source_text=emb_xml,
                            storage_opts=storage_keys,
                            overwrite_opts=overwrite_keys,
                            source_lang_code=metadata['lang_codes'][0],
                            targ_lang_code='en',
                            )

    store_data(storage='dir',
                data=emb_xml,
                dir_path=dir_path,
                name='grobid',
                )

# convert file to text with ocr
    #verbose_mess('Getting txt: '+dir_path, verbose)
    tool_txts = get_txt(dir_path,
                tool_names=conv_tool_names,
                tools=get_funs_from_module(ctools),
                storage_opts=storage_keys,
                overwrite_opts=overwrite_keys,
                )

    store_data(storage='dir',
                data=tool_txts,
                dir_path=dir_path,
                name='ocr_extraction',
                )
    
    txt_trans = dict()
    for tool, ocr_txt in tool_txts.items():
        txt_trans[tool] = get_translation(tool_dir_path=os.path.join(dir_path,tool),
                                source_text=ocr_txt,
                                source_lang_code=metadata['lang_codes'][0],
                                targ_lang_code='en',
                                storage_opts=storage_keys,
                                overwrite_opts=overwrite_keys,
                                )

    store_data(storage='dir',
                data=txt_trans,
                dir_path=dir_path,
                name='translation',
                ) 
                
mess_col('Conversion successful!',col_config['end_col'])