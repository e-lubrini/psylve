import json
import os
import subprocess
import requests

conv_config_path = os.path.join('tools','grobid','grobid_config.json')
with open(conv_config_path, 'r') as config_file:
    config = json.load(config_file)

def extract_emb_txt(pdf_filepath,
                    grobid_inst_path=config['grobid_inst_path'],
                    config_path=config['config_path'],
                    GROBID_URL=config['GROBID_URL'],
                    url=config['url']
                    ):

    subprocess.run(['bash','../grobid/gradlew run'])

    xml = requests.post(url, files={'input': open(pdf_filepath, 'rb')})

    return xml.text