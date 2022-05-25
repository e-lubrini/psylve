import os
import fnmatch
import shutil

trans_name = 'translation.txt'
data_path = '/home/elubrini/GitHub/psylloidea_ontology/pdf2txt/data/docs_for_conv'

def get_files(treeroot, pattern):
    results = []
    for base, dirs, files in os.walk(treeroot):
        goodfiles = fnmatch.filter(files, pattern)
        results.extend(os.path.join(base, f) for f in goodfiles)
    print('FILES: ',len(results))
    return results

trans_files = get_files(data_path, trans_name)
target_folder='/home/elubrini/GitHub/psylloidea_ontology/pdf2txt/data/translations'

for t in trans_files:
    path = os.path.normpath(t)
    path_sects = path.split(os.sep)
    target_name = path_sects[-3]+'_translation.txt'
    target_path = os.path.join(target_folder,target_name)
    print(target_path)
    shutil.copyfile(t, target_path)