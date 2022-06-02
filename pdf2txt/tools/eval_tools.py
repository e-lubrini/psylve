import os
from tools.utils import try_read, true_counter, mkdir_no_over, get_child_ext_path
from tools.pdf_tools import prep_and_tokenise, read_doc_metadata
import random
import json
from enchant.checker import SpellChecker
from tqdm.notebook import tqdm

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

def spellcheck_score(conv_txt, meta_path, max_words_per_doc):
    # get list of words in the document
    _,doc_wordlist = prep_and_tokenise(conv_txt)
    if max_words_per_doc:
        doc_wordlist_sample = []
        for _ in range(max_words_per_doc):
            doc_wordlist_sample.append(random.choice(doc_wordlist))
        doc_wordlist = doc_wordlist_sample
    # get lang code for spell checker
    metadata = read_doc_metadata(meta_path, path_type='meta')
    lang_codes = metadata['lang_codes']
    for lang_code in lang_codes:
        try:
            cc = true_counter(funcQ=word_is_correct_Q, elems=doc_wordlist, lang_code=lang_code)
            tc = len(doc_wordlist)
        except:
            print('Warning: dictionary for {0} not installed. install it via aspell/hunspell/myspell.'.format(lang_code))
            print('e.g. sudo apt install aspell-{0}'.format(lang_code))
    return cc/(tc+1)

     
############################
## EVALUATE TOOLS ON DATA ##
############################
def eval_tools_scores(dir_paths,
                        score_names,
                        scoring_funs,
                        conv_tool_names=[],
                        store_path='',
                        max_words_per_doc=None,
                        ):
    scores_filepath = os.path.join(store_path,'scores.json')
    scores_by_tool = try_read(scores_filepath, alt={})
    if type(scores_by_tool) == str:
        scores_by_tool = json.loads(scores_by_tool)
    mkdir_no_over(store_path)
    for dir_path in tqdm(dir_paths):
        for tool_name in conv_tool_names:
            conv_txt_path = get_child_ext_path(os.path.join(dir_path,tool_name), ['.txt']) 
            with open(conv_txt_path, 'r') as f:
                conv_txt = f.read()
            meta_path = get_child_ext_path(dir_path, ['.json'])
            for score_name in score_names:
                if (score_name not in scores_by_tool.keys()) or (tool_name not in scores_by_tool[score_name].keys()):
                    try:
                        scores_by_tool[score_name]
                    except KeyError:
                        scores_by_tool[score_name] = dict()
                    scoring_fun = scoring_funs[score_name]
                    score = scoring_fun(conv_txt, meta_path, max_words_per_doc)
                    
                    try:
                        scores_by_tool[score_name][tool_name] *= score
                    except KeyError:
                        scores_by_tool[score_name][tool_name] = score
                    with open(scores_filepath, 'w+') as f:
                        json.dump(scores_by_tool, f)
    return scores_by_tool

    

