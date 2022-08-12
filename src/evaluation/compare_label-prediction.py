#!/bin/env python

import csv
import sys
import json
import math


# ./compare-psylle.py Cpruni_occurrences_binary.json extracted_psyllid_entities.txt extracted_psyllid_relations.txt >eval.json


# Either reference and prediction document names are the same
def same_doc(ref, pred):
    return pred == ref or pred == ref + '_translation'


# Similarity between vactors
def sim_vector(ref, pred):
    if ref['acceptedNameUsage'] == pred['CANONICAL']:
        return 1.0
    return 0.0
    

# Similarity between locations
def sim_location(ref, pred):
    if ref['country'].lower() == pred['FORM'].lower():
        return 1.0
    return 0.0


# Similarity between hosts
def sim_host(ref, pred):
    if ref['hostPlantLatinName'] == pred['CANONICAL']:
        return 1.0
    return 0.0


# Similarity between dates
def sim_date(ref, pred):
    if ref['eventDate'] == pred['FORM']:
        return 1.0
    return 0.0


TYPES = ('vector', 'location', 'host', 'date')


class hashabledict(dict):
    def __hash__(self):
        return hash(tuple(sorted(self.items())))


with open(sys.argv[1]) as f:
    reference = json.load(f)
ref_documents = set(ref['common']['filename'] for ref in reference)
ref_entities = set()
for ref in reference:
    fn = ref['common']['filename']
    ref_entities.add(hashabledict(ref['left']))
    ref_entities.add(hashabledict(ref['right']))


with open(sys.argv[2], newline='') as f:
    entcsv = csv.DictReader(f, delimiter='\t')
    pred_entities = set(hashabledict(row) for row in entcsv)


with open(sys.argv[3], newline='') as f:
    relcsv = csv.DictReader(f, delimiter='\t')
    pred_relations = set(hashabledict(row) for row in relcsv)


sim_fun = {
    'vector': sim_vector,
    'location': sim_location,
    'host': sim_host,
    'date': sim_date
}


def sim(ref, pred):
    if ref['type'] != pred['TYPE']:
        return 0.0
    if not same_doc(ref['filename'], pred['DOC']):
        return 0.0
    return sim_fun[ref['type']](ref, pred)


def find_best_ent(paired_pred, ref_ent):
    max_sim = 0.0
    best_pred = None
    for pred_ent in pred_entities:
        if pred_ent in paired_pred:
            continue
        s = sim(ref_ent, pred_ent)
        if s == 0.0:
            continue
        if s > max_sim:
            max_sim = s
            best_pred = pred_ent
    return best_pred, max_sim


def pair_filter(pair, doc=None, type_=None, cat=None):
    r = pair['ref']
    p = pair['pred']
    if doc is not None:
        if r is not None and r['filename'] != doc:
            return False
        if p is not None and not same_doc(doc, p['DOC']):
            return False
    if type_ is not None:
        if r is not None and r['type'] != type_:
            return False
        if p is not None and p['TYPE'] != type_:
            return False
    if cat is not None:
        return cat == pair['cat']
    return True


TRUE_POSITIVE = 'True Positive'
FALSE_POSITIVE = 'False Positive'
FALSE_NEGATIVE = 'False Negative'


ent_pairs = []
paired_pred = set()
for ref_ent in ref_entities:
    pred_ent, s = find_best_ent(paired_pred, ref_ent)
    if pred_ent is not None:
        paired_pred.add(pred_ent)
        cat = TRUE_POSITIVE
    else:
        cat = FALSE_NEGATIVE
    ent_pairs.append({'ref': ref_ent, 'pred': pred_ent, 'sim': s, 'cat': cat})
for pred_ent in pred_entities:
    if pred_ent not in paired_pred:
        ent_pairs.append({'ref': None, 'pred': pred_ent, 'sim': 0.0, 'cat': FALSE_POSITIVE})


def evaluate(pairs):
    tp = list(p for p in pairs if pair_filter(p, cat=TRUE_POSITIVE))
    fp = list(p for p in pairs if pair_filter(p, cat=FALSE_POSITIVE))
    fn = list(p for p in pairs if pair_filter(p, cat=FALSE_NEGATIVE))
    if len(tp) + len(fn) == 0:
        recall = math.nan
    else:
        recall = float(len(tp)) / (len(tp) + len(fn))
    if len(tp) + len(fp) == 0:
        precision = math.nan
    else:
        precision = float(len(tp)) / (len(tp) + len(fp))
    if recall + precision == 0:
        f1 = math.nan
    else:
        f1 = 2 * recall * precision / (recall + precision)
    return recall, precision, f1


ent_eval = {}
for doc in ref_documents:
    ent_doc_eval = {}
    for type_ in TYPES:
        pairs = list(p for p in ent_pairs if pair_filter(p, doc=doc, type_=type_))
        recall, precision, f1 = evaluate(pairs)
        ent_doc_eval[type_] = {
            'pairs': pairs,
            'recall': recall,
            'precision': precision,
            'f1': f1
        }
    ent_eval[doc] = ent_doc_eval
    recall, precision, f1 = evaluate(ent_pairs)
    ent_eval['global'] = {
        'recall': recall,
        'precision': precision,
        'f1': f1
    }


json.dump(ent_eval, sys.stdout, indent=4)
