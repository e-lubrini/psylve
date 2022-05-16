import os
from inspect import getmembers, isfunction
from tools import eval_tools
from tools.utils import *
from enchant.checker import SpellChecker
import tqdm

#######################
## SCORING FUNCTIONS ##
#######################

## spellcheck_score
def word_is_correct_Q(w,
                    lang_code,
                    max_error_allowed = 0,
                    ):
    d = SpellChecker(lang_code)
    d.set_text(w)
    errors = [err.word for err in d]
    if (len(errors) <= max_error_allowed):
        return True
    else:
        return False
def spellcheck_score(conv_txt_path, meta_path):
    # get list of words in the document
    with open(conv_txt_path, 'r') as f:
        conv_txt = f.read()
    _,doc_wordlist = prep_and_tokenise(conv_txt)
    # get lang code for spell checker
    metadata = read_doc_metadata(meta_path, path_type='meta')
    lang_codes = metadata['lang_codes']
    for lang_code in lang_codes:
        try:
            c = true_counter(funcQ=word_is_correct_Q, elems=doc_wordlist, lang_code=lang_code)
        except:
            print('Warning: dictionary for {0} not installed. install it via aspell/hunspell/myspell.'.format(lang_code))
            print('e.g. sudo apt install aspell-{0}'.format(lang_code))
    return c

     
############################
## EVALUATE TOOLS ON DATA ##
############################
def eval_tools_scores(db_dir_path,
                        conv_tool_names, # tools to be evaluated
                        score_names,
                        scoring_funs,
                        ):
    scores_by_tool = dict()
    for dir_path in tqdm(get_child_dir_paths(db_dir_path)):
        for tool_name in conv_tool_names:
            conv_txt_path = get_child_ext_path(os.path.join(dir_path,tool_name), ['.txt']) 
            meta_path = get_child_ext_path(dir_path, ['.json'])
            for score_name in score_names:
                try:
                    scores_by_tool[score_name]
                except KeyError:
                    scores_by_tool[score_name] = dict()
                    
                scoring_fun = scoring_funs[score_name]
                score = scoring_fun(conv_txt_path, meta_path)
                try:
                    scores_by_tool[score_name][tool_name] += score
                except KeyError:
                    scores_by_tool[score_name][tool_name] = score
    return scores_by_tool

