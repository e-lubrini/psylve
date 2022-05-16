import os
import fastwer
from numpy import source

def tool_cer(cers,
            name,
            tool_name, 
            text,
            dir_path,
            ref_dir):

    ref = os.listdir(os.path.join(dir_path, ref_dir))[0]
    output = text
    try:
        score = fastwer.score_sent(output, ref, char_level=True)
        cers[name][tool_name] = score
    except TypeError:
        print('Tried to pass None to score function')
    
    return cers

def get_cer(cers,
        doc_object,
        dir_path,
        ref_dir,
        source='file'):
    
    '''takes a dict where to store the CERs, the doc object, its path and the name of the reference folder
    returns the dictionary of CERs updated with the new score'''

    name = doc_object.input_filename
    cers[name] = {}

    if source == 'file':
        for tool_name in [tool_name for tool_name in os.listdir(dir_path) if os.path.isdir(os.path.join(dir_path, tool_name)) if tool_name != ref_dir]:
            tool_path = os.path.join(dir_path,tool_name)
            for file in os.listdir(tool_path):
                conv_filepath = os.path.join(tool_path,file)
                break
            with open(conv_filepath,'r') as f:
                text = f.read()
            cers.update(tool_cer(cers, name, tool_name, text, dir_path, ref_dir))

    elif source == 'obj':
        for tool_name,text in doc_object.data['txt'].items():
            cers.update(tool_cer(cers, name, tool_name, text, dir_path, ref_dir))

    return cers
