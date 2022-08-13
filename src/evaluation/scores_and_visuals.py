import sys
import json
from types import NoneType
import pandas as pd
import seaborn as sns
import math
from sklearn.metrics import confusion_matrix, classification_report, make_scorer, f1_score, recall_score, precision_score

sys.stdout.write('COMPUTING SCORES\n')



####################
## Subdirectories ##
####################
import os

def get_child_dir_paths(dir_path):
    child_names = os.listdir(dir_path)
    child_paths = [os.path.join(dir_path,child_name) for child_name in child_names]
    dir_paths = [child_path for child_path in child_paths if os.path.isdir(child_path)]
    return dir_paths

pred_dir_path = 'data/pred'

comp_filepaths = dict()

c = 0

for dirpath in get_child_dir_paths(pred_dir_path):
    comp_filepath = []
    for filepath in os.listdir(dirpath):
        filepath = os.path.join(pred_dir_path,str(c),filepath)
        if 'comp' in filepath:
            comp_filepath.append(filepath)

        comp_filepaths[c] = comp_filepath
    c += 1

# e.g. of pred_filepaths:
# {0: [('data/pred/0/extracted_psyllid_entities.txt',
#    'data/pred/0/extracted_psyllid_relations.txt')],
#  1: [('data/pred/1/extracted_psyllid_entities.txt',
#    'data/pred/1/extracted_psyllid_relations.txt')]}

save_dir = 'data/evaluation_results/'


#######################
##### nested  dict ####
##### to dataframe ####
#######################


ref_df = dict(docname=[], entname=[], dir_n=[])
pred_df = dict(docname=[], entname=[], dir_n=[])

with open('data/comparison.json', 'r') as f:
    ent_evals = json.load(f)

for dir_n,comp_filepath in comp_filepaths.items():

    #open each json comparison.json file
    with open(comp_filepath[0], 'r') as f:
            ent_eval = json.load(f)
    len(ent_eval.items())
    if 'global' in ent_eval.keys():
        ent_eval.pop('global')

    for docname,entities in ent_eval.items():
        if docname == 'global':
            continue 
        for entname,pairs_n_scores in entities.items():
            if pairs_n_scores is NoneType:
                continue
            else:
                for pair in pairs_n_scores['pairs']:
                    #print((pair.keys())) # = 'ref', 'pred', 'sim', 'cat'
                    
                    try:
                        pair['ref'].items()
                        pair['pred'].items()
                    except AttributeError:
                        continue
                    for a,v in pair['ref'].items(): # attribute and value of entity
                        if a not in ref_df.keys():
                            ref_df[a] = []
                        ref_df[a].append(v)

                    for a,v in pair['pred'].items():
                        if a not in ref_df.keys():
                            pred_df[a] = []
                        pred_df[a].append(v)

                    ref_df['dir_n'].append(dir_n)
                    pred_df['dir_n'].append(dir_n)

                    ref_df['docname'].append(docname)
                    pred_df['docname'].append(docname)
                    
                    pred_df['entname'].append(entname)
                    ref_df['entname'].append(entname)

                    
                    sizes = []
                    for k in ref_df.keys():
                        sizes.append(len(ref_df[k]))
                    for k in ref_df.keys():
                        if len(ref_df[k]) < max(sizes):
                            ref_df[k].extend([math.nan]*(max(sizes) - len(ref_df[k])))
                    sizes = []
                    for k in pred_df.keys():
                        sizes.append(len(pred_df[k]))
                    for k in pred_df.keys():
                        if len(pred_df[k]) < max(sizes):
                            pred_df[k].extend([math.nan]*(max(sizes) - len(pred_df[k])))
            

ref_df = pd.DataFrame(ref_df)
pred_df = pd.DataFrame(pred_df)

################
## DUMMY DATA ##
################

## Create dummy data to be visualised using sklearn tools.

dummies = {'False Positive': (0,1),
            'False Negative': (1,0),
            'True Positive': (1,1),
            'True Negative': (0,0),
            }

dummies_inv = {v: k for k, v in dummies.items()}

def create_dummy(data):
    dummy_data = []
    for docname,entities in data.items():
        if (type(entities) is float) or (type(entities) is list):
            continue
        for entname,pairs_n_scores in entities.items():
            if (type(pairs_n_scores) is float) or (type(pairs_n_scores) is list):
                continue
            for pair in pairs_n_scores['pairs']:
                label = pair['cat']
                dummy_data.append(dummies[label])

    dummy_df = pd.DataFrame(dummy_data, columns =['ref', 'pred'])
    
    return dummy_df

dummies_df = dict()
for k,ent_eval in ent_evals.items():
    dummies_df[k] = create_dummy(ent_eval)

## dummies_df.keys() are numbers of folders

for k,dummy_df in dummies_df.items():
    ref_dummy, pred_dummy = dummy_df['ref'], dummy_df['pred']
    dummies_df[k]=list(zip(ref_dummy, pred_dummy))


# plotting confusion matrix
conf_mat = confusion_matrix(ref_dummy, pred_dummy)
sns.set(font_scale=1)
matrix = sns.heatmap(conf_mat, annot=True, fmt='d', linewidths=.5, cmap='flare')
matrix.set(xlabel='predicted', ylabel='actual')
matrix.figure.savefig("data/evaluation_results/confusion_matrix.png") 

print(classification_report(ref_dummy, pred_dummy))



#############
## VISUALS ##
#############

from collections import Counter
from tools.visual import plot

counts =dict()

for k,dummy_df in dummies_df.items():
    counts[k] = dict(Counter(dummy_df))
print(counts)

df = pd.DataFrame([count.values() for count in counts.values()],columns=[dummies_inv[k] for k in counts['0'].keys()])
#df = df.reset_index()
df

rows = []
for col_name in df.columns:
    col = df[col_name]
    for i in df.index:
        rows.append((i,col_name,df[col_name].iloc[i]))

df = pd.DataFrame(rows, columns=['i','cat','val'])


x = 'i'
hue = 'cat'
palette = sns.color_palette('tab10',n_colors=2)

plot(x=x, hue=hue, data=df,
    title = 'Feature impact' ,
    type='dist',
    save_dir = save_dir,
    )

matrix.figure.savefig("data/evaluation_results/confusion_matrix.png") 