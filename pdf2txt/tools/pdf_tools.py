import imp
from tools.utils import try_read, get_funs_from_module, get_dir_and_doc_paths, get_child_ext_path
import tools.eval_tools as etools

import json 
import fitz
import fasttext
import os
import string


###############
## PDF TOOLS ##
###############
# extract embedded text
def get_emb_txt(path):
    _, doc_path = get_dir_and_doc_paths(path)
    try:
        metadata = read_doc_metadata(path=doc_path, path_type='doc')
        text = metadata['emb_text']
    except:
        text = ""
        doc = fitz.open(doc_path)
        for page in doc:
            text += page.get_text().replace('\n',' ')
    return text

# tokenise and preprocess text
def prep_and_tokenise(text):
    doc_wordlist = list(set(text.translate(str.maketrans('', '', string.punctuation)).lower().replace('\n',' ').split()))
    prep_text = ' '.join(doc_wordlist).replace('\n',' ')
    return prep_text, doc_wordlist

# find language(s) of a text
def get_langs(prep_text,     # text whose language is to be detected
            lang_n=1    # how many possible lang_codes we want to detect (in order from most to least probable)
            ):
    model = fasttext.load_model(os.path.join('models','lid.176.ftz'))
    prediction = (model.predict(prep_text, k=lang_n))[0] # tuple of language codes and respective probabilities
    lang_codes = [label[-2:] for label in prediction]
    return lang_codes    # list of language code(s) detected

                
##############
## METADATA ##
##############
def write_pdf_metadata(path, overwrite_keys):
    dir_path, filepath = get_dir_and_doc_paths(path)
    # info to be stored
    metadata = get_metadata(filepath, overwrite_keys)
    # write metadata file
    meta_path = os.path.join(dir_path, 'metadata.json')
    with open(meta_path, 'w') as f:
        json.dump(metadata, f, indent = 4)
    return metadata

def get_meta_path(path, path_type):
    path_types = ['doc', # the document being treated
                'meta', # the metadata file
                'dir'] # the directory where the metadata is stored
    if path_type not in path_types:
        raise ValueError("Invalid path_type. Expected one of: {0}".format(path_types)) 
    match path_type:
        case 'doc': 
            dir_path = os.path.split(path)[-2]
            meta_path = get_child_ext_path(dir_path, '.json')
        case 'meta':
            meta_path = path
        case 'dir':
            dir_path = path
            meta_path = get_child_ext_path(dir_path, '.json')
    return meta_path

def read_doc_metadata(path, path_type):
    meta_path = get_meta_path(path, path_type=path_type)
    with open(meta_path) as f:
        metadata = json.load(f)
    return metadata

def get_metadata(dir_path,
                storage_opts,
                overwrite_opts,
                threshold,
                ):
    try:
        meta_path = get_meta_path(dir_path, path_type='dir')
        with open(meta_path) as f:
            metadata = json.load(f)
    except (IndexError, FileNotFoundError):
        metadata = dict()

    metadata['emb_txt'] = get_emb_txt(dir_path)
    if storage_opts['lang_codes'] and (overwrite_opts['lang_codes'] or not ('lang_codes' in metadata.keys())):
        prep_txt,_ = prep_and_tokenise(metadata['emb_txt'])
        metadata['lang_codes'] = get_langs(prep_txt)
    
    pop_keys = set()
    for k in metadata.keys():
        pop_keys.add if k not in storage_opts.keys() else None
    for k in pop_keys:
        metadata.pop(k, None)

    # check if emb text is usable
    if storage_opts['emb_txt_ok'] and (overwrite_opts['emb_txt_ok'] or not ('emb_txt_ok' in metadata.keys())):
        metadata['score'] = eval_txt(dir_path=dir_path,
                                    text=metadata['emb_txt'], # tools to be evaluated
                                    score_names=['spellcheck_score'],
                                    scoring_funs= get_funs_from_module(etools),
                                    )['spellcheck_score']
        metadata['emb_txt_ok'] = metadata['score'] >= threshold

    return metadata
    

# add metadata entry
def add_metadata_entry(dir_path,
                        entry_name,
                        entry_cont,
                        ):
    metadata = read_doc_metadata(dir_path, path_type='dir')
    meta_path = get_meta_path(dir_path, path_type='dir')
    metadata[entry_name] = entry_cont
    with open(meta_path, 'w') as f:
        json.dump(metadata, f, indent = 4)

# evaluate text
def eval_txt(dir_path,
            score_names,
            scoring_funs,
            text='',
            max_words_per_doc=None,
            ):
    scores_filepath = os.path.join(dir_path,'scores.json')
    scores_by_tool = try_read(scores_filepath, alt={})
    if type(scores_by_tool) == str:
        scores_by_tool = json.loads(scores_by_tool)
    meta_path = get_child_ext_path(dir_path, ['.json'])
    for score_name in score_names:
        if score_name not in scores_by_tool.keys():
            try:
                scores_by_tool[score_name]
            except KeyError:
                scores_by_tool[score_name] = 0
            scoring_fun = scoring_funs[score_name]
            score = scoring_fun(text, meta_path, max_words_per_doc)
            scores_by_tool[score_name] += score
    return scores_by_tool