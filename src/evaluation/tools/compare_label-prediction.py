#!/bin/env python

import os

import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns

import os
import csv
import sys
import json
import math
from nltk.tokenize import word_tokenize

from pathlib import Path

from tools.visual import *

pred_dir_path = 'data/pred'
save_dir = 'data/img/evaluation/'
eval_db_path = '/home/elubrini/GitHub/psylve/src/text_extraction/data/15/txt/'

# ./compare-psylle.py Cpruni_occurrences_binary.json extracted_entities.txt extracted_relations.txt >eval.json

sys.stdout.write('COMPARISON STARTED\n')
ref_filepath = 'data/ref/cpruni_occurrences_binary.json'
sys.stdout.write(ref_filepath) # label filepath

#########################
## Load Subdirectories ##
#########################

# each subdirectory is an output of a variation of the same pipeline
# with different strategies implemented (for comparison)


def get_child_dir_paths(dir_path):
    child_names = os.listdir(dir_path)
    child_paths = [os.path.join(dir_path,child_name) for child_name in child_names]
    dir_paths = [child_path for child_path in child_paths if os.path.isdir(child_path)]
    return dir_paths

def get_child_filepaths(dir_path):
    path_list = [filenames for dirpath, dirnames, filenames in os.walk(dir_path)]
    return path_list


######################
## Load Predictions ##
######################

## list filepaths of predictions
## both entities and relations
print(eval_db_path)
eval_db_paths = get_child_filepaths(eval_db_path)
print(eval_db_paths)
pred_filepaths = dict()

c = 0 # subdirectories are named sequentially starting from 0
for dirpath in get_child_dir_paths(pred_dir_path):
    pred_ent_filepaths = []
    pred_rel_filepaths = []
    for filepath in os.listdir(dirpath):
        filepath = os.path.join(pred_dir_path,str(c),filepath)
        
        if 'ent' in filepath:
            pred_ent_filepaths.append(filepath)
        elif 'rel' in filepath:
            pred_rel_filepaths.append(filepath)

        pred_filepaths_in_dir = list(zip(pred_ent_filepaths, pred_rel_filepaths))
        pred_filepaths[c] = pred_filepaths_in_dir
    c += 1

    # e.g. of pred_filepaths:
    # {0: [('data/pred/0/extracted_entities.txt', # pipeline version 0, entities
    #    'data/pred/0/extracted_relations.txt')], # pipeline version 0, relations
    #  1: [('data/pred/1/extracted_entities.txt', # pipeline version 1, entities
    #    'data/pred/1/extracted_relations.txt')]} # pipeline version 1, relations


## load content of reference data

#reference_nomeclature_db_filepath = '../../../text-mining-workflow/ancillaries/psylve/psyllist_tokens.txt'
#with open(reference_nomeclature_db_filepath, 'r') as f:
#    reference_nomeclature_db = f.read()

#TODO save data to be used by scores and visual script