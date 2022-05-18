# Psylloidea Ontology (WIP)
## ontology in progress of construction...
Ontology Learning project @ CIRAD, and INRAE for an ontology of superfamily Psylloidea with a focus on its role as vecor of phythoplasma.

## Repository Structure

    text_extraction/
        ├── data/
        ├── evaluation_results/
        ├── models/
        ├── tools/
        |   ├── grobid_client_python/
        |   ├── conv_tools.py
        |   ├── eval_tools.py
        |   └── utils.py
        ├── config.json
        ├── conversion_pipeline.py
        ├── evaluation_pipeine.ipynb
        └── start_conversion.sh

## Text Extraction
### Requirements
This pipeline requires a Python version of at least 3.10.

Install Python packages.
```pip install -r pip_requirements.txt```
Install APT packages.
```sed 's/#.*//' apt_requirements.txt | xargs sudo apt-get install```
[//]: # (comm -12 <(apt-mark showmanual | sort) <(grep " install " /var/log/dpkg.log | cut -d " " -sf4 | grep -o "^[^:]*" | sort) > path_to/apt_requirements.txt)
Clone required GitHub repositories.

`cd [path_to]/tools` (or a different path, then changing the relative _.grobid.config_path_ value within the config.json file) and install _grobid_client_python_ by following the [instructions](https://github.com/kermitt2/grobid_client_python)
```
git clone https://github.com/kermitt2/grobid_client_python
cd grobid_client_python
python3 setup.py install
```
### Configuration


### Usage
`mkdir /data/docs_for_conv` (or a different path, then changing the relative _.dataset.path_ value within the config.json file) and add the documents to be converted to the folder. 

```bash start_conversion.sh -c config.json``` or run the script with the `-h` flag to get help with the possible commands.

The chosen folder for the data input will be populated with a directory for each document, containing: the inputted document, a metadata file, a folder for each OCR tool (containing txt files of both the extracted text and the translation to english of such text). 

#### Converted data path structure

    /data/docs_for_conv/
        ├── DocumentName1/
        |   ├── OCRToolName/
        |   |   ├── conversion.txt
        |   |   └── translation.txt
        |   ├── OriginalDocument.pdf
        |   └── metadata.json
        |
        └── DocumentName2/
            ├── ...
