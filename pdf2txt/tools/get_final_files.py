import os
import fnmatch
import shutil
from utils import mkdir_no_over


def get_final_files(treeroot, pattern):
    results = []
    for base, dirs, files in os.walk(treeroot):
        goodfiles = fnmatch.filter(files, pattern)
        results.extend(os.path.join(base, f) for f in goodfiles)
    print('{0} FILES FOUND'.format(len(results)))
    return results

def store_final_files(final_files, target_folder):
    for t in final_files:
        path = os.path.normpath(t)
        path_sects = path.split(os.sep)
        target_name = path_sects[-3]+'_'+final_name
        target_path = os.path.join(target_folder,target_name)
        shutil.copyfile(t, target_path)

final_name = 'translation.txt'
data_path = '/home/elubrini/GitHub/psylve/pdf2txt/data/docs_for_conv'
target_folder=mkdir_no_over('/home/elubrini/GitHub/psylve/pdf2txt/data/final/')

store_final_files(final_name, data_path, target_folder)