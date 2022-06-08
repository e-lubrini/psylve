#############
## IMPORTS ##
#############

from tools.utils import colours
from tools.utils import *

from tools.conv_tools import *
from tools import conv_tools as ctools

from tools.eval_tools import *
from tools.pdf_tools import *

import csv
from statistics import mean

from tqdm import tqdm
import time

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-c')
parser.add_argument('-v', action='store_true')
parser.add_argument('-t', action='store_true')
args = parser.parse_args()

arguments = {'c': args.c, 'v': args.v, 't': args.t}

#############
## CONFIGS ##
#############
# open configuration file from path
config_file_path = args.c
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
if args.v:
    verbose = colours[mess_cols['verbose']]
else:
    verbose = False
if args.t:
    time_verb = colours[mess_cols['time_verb']]
else:
    time_verb = False

#preferences
ocr_if_emb_txt_ok = configs['extraction']['ocr_if_emb_txt_ok'] # still extract with ocr, even if the embedded text is good

# names
name_configs = configs['naming']
final_name = name_configs['files']['final_name']
embedded_text_quality = name_configs['metadata']['embedded_text_quality_score']
meta_name = name_configs['files']['metadata']

# paths and tools
input_dir_path = configs['dataset_paths']['docs_for_extraction']
dbg(input_dir_path)
conv_tool_names = configs['extraction']['tool_names']
dbg(conv_tool_names)
target_folder = configs['dataset_paths']['target_folder']
meta_filepath = target_folder+meta_name+'.csv'

# metadata
threshold = int(configs['extraction']['emb_txt_ok_threshold'])
meta_keys = configs['naming']['metadata'].values()

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

# setup
max_embedded_text_quality = 0
avg_embedded_text_quality = 0
with open(meta_filepath,'w') as f: # create summary metadata
    writer = csv.DictWriter(f, fieldnames=meta_keys)
    writer.writeheader() 

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

img2pdf_paths = [p for p in list(map(ctools.img2pdf, not_pdf_filepaths)) if p is not None] # convert to pdf
dbg(img2pdf_paths)
dbg(str(*img2pdf_paths), 'FLATTENED')
verbose_mess('Images to be converted:\n{0}'.format(str((' \n'.join(*img2pdf_paths)))),
                verbose)
                
## REARRANGE FOLDER STRUCTURE
mess_col('Rearranging folder structure...',col_config['header_col'])
pdf_filepaths = list_ext(input_dir_path,
                        exts=['pdf'],
                        invert=False,
                        )
for pdf_filepath in pdf_filepaths:
    mv_to_custom_dir(pdf_filepath)

# list files by size
sorted_dirs = sorted(get_child_dir_paths(input_dir_path),
                        key =  lambda x: os.stat(get_child_ext_path(x, '.pdf')).st_size)

tot_size = sum(list(map(lambda x: os.stat(get_child_ext_path(x, '.pdf')).st_size, get_child_dir_paths(input_dir_path))))
verbose_mess('Total dataset size: {0}'.format(hr_size(tot_size)),
                verbose)

## START EXTRACTING DATA
mess_col('Extracting text...',col_config['header_col'])
start_time = time.time()
size_left = tot_size
size_done = 0
for dir_path in tqdm(sorted_dirs, total=len(sorted_dirs), desc='processed documents: ', leave=True, mininterval=0, miniters=1):
    size = os.stat(get_child_ext_path(dir_path, '.pdf')).st_size
    verbose_mess('Processing:\n\tsize {0};\n\tpath {1}'.format(hr_size(size),dir_path),
                verbose)

# compile metadata for each file
    # TODO verbose need metadata, etc.
    verbose_mess('Getting metadata', verbose)
    metadata = get_metadata(dir_path,
                            storage_opts=storage_keys,
                            overwrite_opts=overwrite_keys,
                            threshold=threshold
                            )
    store_data(storage='meta',
                data=metadata,
                dir_path=dir_path,
                name='metadata',
                )
    verbose_mess('\tEmbedded text quality score: {0}%\n\t\tcurrent highest: {1}\n\t\tcurrent average: {2})'.format(metadata[embedded_text_quality]*100, max_embedded_text_quality,avg_embedded_text_quality), verbose)
    
    max_embedded_text_quality = max([metadata[embedded_text_quality],max_embedded_text_quality])
    avg_embedded_text_quality = mean([avg_embedded_text_quality,metadata[embedded_text_quality]])
    if metadata[embedded_text_quality] >= threshold or ocr_if_emb_txt_ok:
    # extract embedded xml and translate to English
        verbose_mess('Getting emb xml', verbose)
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

# extract text from file with ocr
    verbose_mess('Getting ocr txt', verbose)
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
    verbose_mess('Getting ocr txt translation', verbose)
    txt_trans = dict()
    for tool, ocr_txt in tool_txts.items():
        txt_trans[tool] = get_translation(tool_dir_path=os.path.join(dir_path,tool),
                                        source_text=ocr_txt,
                                        source_lang_code=metadata['lang_codes'][0],
                                        targ_lang_code='en',
                                        storage_opts=storage_keys,
                                        overwrite_opts=overwrite_keys,
                                        )
    trans_name = 'translation'
    store_data(storage='dir',
                data=txt_trans,
                dir_path=dir_path,
                name=trans_name,
                ) 
    
    runtime_sec = time.time() - start_time
    size_done += size
    size_left -= size
    processing_rate = size_done/runtime_sec
    if processing_rate > 5000: # if rate is too high, documents so far haven't needed any processing, so timing for estimation is reset until first processable document
        size_done = 0
        start_time = time.time()
    else:
        verbose_mess(('Processing rate: {0}/h\t {1}/{2} left'.format(hr_size(processing_rate*3600), ''.join(list(filter(lambda x: not x.isalpha(), hr_size(size_left)))), hr_size(tot_size))), time_verb)
        verbose_mess('Estimated time left: {0}'.format(hr_time(size_left/processing_rate)), time_verb)

# update summary metadata
    with open(meta_filepath,'a') as f:
        writer = csv.DictWriter(f, fieldnames=meta_keys)
        writer.writerow(metadata)

## STORING DATA
mess_col('Storing final files...',col_config['header_col'])
mkdir_no_over(target_folder)
store_final_files(final_name, input_dir_path, target_folder)

mess_col('Extraction successful!',col_config['end_col'])