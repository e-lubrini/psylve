
from importlib.metadata import metadata
from inspect import getmembers, isfunction
import functools
import os
import string

import json

import fitz
import fasttext
fasttext.FastText.eprint = lambda x: None

import enchant
from enchant.checker import SpellChecker
from enchant.errors import DictNotFoundError, DefaultLanguageNotFoundError

from tqdm import tqdm

from nltk.corpus import words
from nltk.tokenize import sent_tokenize
import nltk
#nltk.download('words')

from deep_translator import GoogleTranslator

from time import sleep
import inspect
import functools

###########
## DEBUG ##
###########
def get_var_name(var):
    try:
        callers_local_vars = inspect.currentframe().f_back.f_back.f_locals.items()
        var = [var_name for var_name, var_val in callers_local_vars if var_val is var][0]
    except IndexError:
        callers_local_vars = inspect.currentframe().f_back.f_locals.items()
        var = [var_name for var_name, var_val in callers_local_vars if var_val is var][0] 
    return str(var)

def dbg(mess, title=''):
    #subprocess.Popen(['echo', str('\033[35m'+ str(title)+'\033[32m'+ str(get_var_name(mess)+': '+'\033[0m'+str(mess)))])
    print(str('\033[35m'+ str(title)+'\033[32m'+ str(get_var_name(mess)+': '+'\033[0m'+str(mess))))
    return

def verbose_mess(mess, verbose):
    if verbose:
        mess_col(mess, verbose)

colours = dict(black = "30m",
                red = "31m",
                green = "32m",
                yellow = "33m",
                blue = "34m",
                magenta = "35m",
                cyan = "36m",
                white = "37m",
                grey = "38m",
                )

def mess_col(mess,col):
    print('\033[0;{0} {1}. \033[0m'.format(col, mess))
    return

#############
## GENERAL ##
#############
def get_funs_from_module(module):
    funs_raw = getmembers(module,isfunction)
    funs = dict()
    for n,t in funs_raw:
        funs[n] = t
    return funs

def true_counter(funcQ, elems, **kwargs):
    c = sum([funcQ(e,**kwargs) for e in elems])
    return c

#######################
## PATH MANIPULATION ##
#######################
def join_parentpath_childnames(parentpath,childnames):
    fullpaths = map(functools.partial(os.path.join,
                        parentpath),
        childnames)
    return list(fullpaths)


# lists paths with certain extension 
def list_ext(path,
            exts,
            invert=False): # return files WITHOUT such extensions instead
    path_list = list()
    for ext in exts:
        if type(ext) == list:
            ext = ext[0]
        for filename in os.listdir(path):
            filepath = os.path.join(path,filename)
            ends_ext = filepath.endswith(ext)
            is_file = os.path.isfile(filepath)
            has_ext = ends_ext and is_file
            if not invert:
                ret_ext = has_ext 
                if ret_ext:
                    path_list.append(filepath)
            elif is_file:
                ret_ext = not has_ext
                if ret_ext:
                    path_list.append(filepath)
    return path_list

# get one child with requested extension
def get_child_ext_path(dir_path, ext):
    child = list_ext(path=dir_path,exts=[ext])[0]
    return child

# creates a folder with the document's name and moves the document in it
def mv_to_custom_dir(doc_path):
    split_path = os.path.split(doc_path)
    ext = os.path.splitext(doc_path)[-1]
    new_dir_name = split_path[-1][:-len(ext)] # same as filename, without the extension
    filename = split_path[-1]
    input_dir_path = split_path[-2]

    new_dir_path = os.path.join(input_dir_path,new_dir_name)
    new_doc_path = os.path.join(new_dir_path,filename)

    if not os.path.exists(new_dir_path):
        os.mkdir(new_dir_path)
    if not os.path.exists(new_doc_path):
        os.rename(doc_path,new_doc_path)
    else:
        print('Warning: a document named {0} already exists. Deleting the newer copy.'.format(filename))
        os.remove(doc_path)
    return
def get_parent_dir(path):
    return os.path.split(path)[-2]

def get_child_dir_paths(dir_path):
    child_names = os.listdir(dir_path)
    child_paths = [os.path.join(dir_path,child_name) for child_name in child_names]
    dir_paths = [child_path for child_path in child_paths if os.path.isdir(child_path)]
    return dir_paths

# make directory if it doesn't exist
def mkdir_no_over(dir_name):
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)

def save_file(filepath, data):
    with open(filepath, 'w+') as f:
        f.write(data)

def save_data(doc_dir,
                dir_name,
                file_name,
                content,
                ):
    dirpath = os.path.join(doc_dir,dir_name)
    mkdir_no_over(dir_name)
    filepath = os.path.join(dirpath,file_name)
    save_data(filepath, content)
    

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

def get_dir_and_doc_paths(path):
    if os.path.isfile(path):
        dir_path = get_parent_dir(path)
        filepath = path
    elif os.path.isdir(path):
        dir_path = path
        filepath = get_child_ext_path(dir_path=dir_path, ext='pdf')
    else:
        print('enter an existing path')
    return dir_path, filepath

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

def get_metadata(dir_path, storage_opts, overwrite_opts):
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
    
    for k in metadata.keys():
        metadata[k].pop(k, None) if k not in storage_opts.keys() else None
    
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

# is emb text usable
def emb_text_is_usable(doc_path, 
                    lang_threshold,
                    lang_wordlist_paths='',
                    sample_size=200,
                    print_score=False,
                    save_emb_text=True):
    text = get_emb_txt(doc_path)
    if text != '':
        
        prep_text, doc_wordlist = prep_and_tokenise(text) # tokenise and preprocess text

        # get language of text
        lang_codes = get_langs(prep_text)

        multilang_score = words_in_langs_ratio(doc_wordlist=doc_wordlist,
                            lang_codes=lang_codes,
                            sample_size=sample_size,
                            lang_wordlist_paths=lang_wordlist_paths
                            )
        if print_score:
            print(multilang_score)
        return multilang_score >= lang_threshold # if not enough words are part of the language...
    else:
        return False

####################
## LANGUAGE TOOLS ##
####################
## functions to check if a word is in a language...
# (a) ...by loading a wordlist
def in_lang_wl(w, lang_code, lang_wordlist_path='', lang_wordlist=[]):
    if not lang_wordlist:
        with open(lang_wordlist_path, 'rU') as f:
            lang_wordlist = set(line.strip() for line in f)
    if w in lang_wordlist:
        return True
    else:
        return False

# (b) ...based on spellcheck
def in_lang_sc(w, lang_code, max_error_count = 0):
    d = SpellChecker(lang_code)
    d.set_text(w)
    errors = [err.word for err in d]
    if (len(errors) <= max_error_count):
        return True
    else:
        return False


# (c) ...based on translation
def translate_wl(lang_code, data_path=None):
    lang_wordlist = set()
    for en_w in tqdm(words.words()):
        translation = (GoogleTranslator('en',lang_code).translate(en_w))
        lang_wordlist.add(translation)

        if data_path:       # if path was specified, save language wordlist
            textfile = open(os.path.join(data_path,'wordlists',(lang_code+'.txt')), "w")
            for w in lang_wordlist:
                textfile.write(w + "\n")
            textfile.close()
        return lang_wordlist

# check words are part of a certain language using one of three methods:
def words_in_lang_ratio(doc_wordlist, lang_code, lang_wordlist, lang_wordlist_path, max_n_words):
    # <(a) wordlist, (b) spellcheck, (c) translation>
    if not enchant.request_dict(lang_code): # show a warning if a dictionary is not installed
        print('WARNING: Install the required dictionary!\ne.g. sudo apt-get install hunspell-{0}'.format(lang_code))
    
    doc_wordlist = doc_wordlist[-max_n_words:]
    ## (a) WORDLIST
    # get wordlist from file ('en.txt' for english, 'fr.txt' for french, etc.)...
    if os.path.exists(lang_wordlist_path):
        # count how many words are also found in the language wordlist
        c = true_counter(func=in_lang_wl, elems=doc_wordlist, lang_wordlist_path=lang_wordlist_path)
        print('COUNT (loaded wordlist):',c)      
    ## (b) SPELLCHECK
    else:       # if there is no wordlist,
        try:    # use spellcheck*
            # count how many words are correct according to language-specific spellcheck
            c = true_counter(func=in_lang_sc, elems=doc_wordlist, lang_code=lang_code)
            print('COUNT (spellchecker):',c)
        except (DictNotFoundError, DefaultLanguageNotFoundError):
            raise Exception('Install the required dictionary!\ne.g. sudo apt-get install hunspell-{0}'.format(lang_code))

    ## (c) TRANSLATE
        # ...if other two methods fail, translate an english wordlist
        # (takes too long; download a list or solve issues with spellchecker, if possible!)
        except AttributeError:
            lang_wordlist = translate_wl(lang_code) # translate an English wordlist to document's language # TODO: support multiple lang_codes per document
            # count how many words are found in the translated language wordlist
            c = true_counter(func=in_lang_wl, elems=doc_wordlist, lang_wordlist=lang_wordlist)
            print('COUNT (translated wordlist):',c)
    try:
        ratio = c/len(doc_wordlist)
    except ZeroDivisionError:
        ratio = 0
    return  ratio

# ratio of words in a list that belong to at least one of listed languages
def words_in_langs_ratio(doc_wordlist,
                        lang_codes,
                        sample_size,
                        lang_wordlist=None,
                        lang_wordlist_paths=None):
    multilang_ratio = 0
    for lang_code in tqdm(lang_codes):
        # calculate the percentage of words recognised by the language
        single_lang_ratio = words_in_lang_ratio(doc_wordlist=doc_wordlist,
                                    lang_code=lang_code,
                                    lang_wordlist=lang_wordlist,
                                    lang_wordlist_path=lang_wordlist_paths[lang_code],
                                    sample_size=sample_size)
        multilang_ratio += single_lang_ratio
    return multilang_ratio

def translate(txt,
            source_lang_code,
            targ_lang_code,
            ):
    sents = sent_tokenize(txt)
    trans_sents = list()
    for sent in sents:
        trans_sent = (GoogleTranslator(source_lang_code,targ_lang_code).translate(str(sent)))
        trans_sents.append(trans_sent)
    translation = ' '.join(trans_sents)
    return translation

# translate conversions to English
def translate_conv(tool_dir_path,
                    output_filename,
                    source_lang_code,
                    targ_lang_code,
                    ):
    conv_path = get_child_ext_path(tool_dir_path, '.txt')
    with open(conv_path, 'r') as f:
        conv_txt = f.read()
    trans_txt = translate(conv_txt, source_lang_code, targ_lang_code)
    trans_path = os.path.join(tool_dir_path, output_filename+'.txt')
    with open(trans_path, 'w+') as f:
        f.write(trans_txt)
    return trans_txt

def translate_meta(dir_path,
                    source_lang_code,
                    targ_lang_code,
                    ):
    metadata = read_doc_metadata(dir_path, path_type='dir')
    emb_txt_trans = translate(metadata['emb_txt'], source_lang_code, targ_lang_code)
    add_metadata_entry(dir_path,
                        'emb_txt_trans',
                        emb_txt_trans,
                        )
    return emb_txt_trans

def translate_doc(dir_path,
                    targ_lang_code='en',
                    output_filename='translation',
                    ):
    # translate conversions to English
    source_lang_code = read_doc_metadata(dir_path, path_type='dir')['lang_codes'][0]
    for tool_dir_path in get_child_dir_paths(dir_path):
        translate_conv(tool_dir_path,
                    output_filename=output_filename,
                    source_lang_code=source_lang_code,
                    targ_lang_code=targ_lang_code,
                    )
    translate_meta(dir_path, source_lang_code, targ_lang_code)
    return