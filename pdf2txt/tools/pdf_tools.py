from tools.eval_tools import *
import tools.eval_tools as etools
from tools.eval_tools import eval_tools_scores

from tools.utils import *

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
            text += page.get_text()
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
        metadata['score'] = eval_tools_scores(dir_paths=dir_path,
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

####################
## LANGUAGE TOOLS ##
####################
def translate_to_lang(txt,
                source_lang_code,
                targ_lang_code,
                ):
    sents = sent_tokenize(txt)
    trans_sents = list()
    for sent in tqdm(sents, desc='translated sentences', leave=False):
        try:
            trans_sent = str((GoogleTranslator(source_lang_code,targ_lang_code).translate(str(sent))))
        except:
            trans_sent = str(sent)
        trans_sents.append(trans_sent)
    translation = ' '.join(trans_sents)
    return translation

# get translation if needed
def get_translation(tool_dir_path,
                    source_text,
                    source_lang_code,
                    targ_lang_code,
                    storage_opts,
                    overwrite_opts,
                    ):
    src_type = get_var_name(source_text)
    translation = try_read(os.path.join(tool_dir_path, 'translation.txt'))
    needs_trans = storage_opts[src_type+'_trans'] and (overwrite_opts[src_type+'_trans'] or not translation)
    if needs_trans:
        translation = translate_to_lang(source_text,
                                        source_lang_code=source_lang_code,
                                        targ_lang_code=targ_lang_code,
                                        )
    return translation