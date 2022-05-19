<h1 align="center">Text Extraction</h1>

## Directory Tree

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

## Requirements
This pipeline requires a Python version of at least 3.10.

#### Install Python packages.
```pip install -r pip_requirements.txt```
#### Install APT packages.
```sed 's/#.*//' apt_requirements.txt | xargs sudo apt-get install```
#### Clone required GitHub repositories.
`cd tools` (or a different path, then changing the relative _.grobid.config_path_ value within the config.json file) and install _grobid_client_python_ by following the [instructions](https://github.com/kermitt2/grobid_client_python)
```
git clone https://github.com/kermitt2/grobid_client_python
cd grobid_client_python
python3 setup.py install
```
## Configuration
Configuration settings can be changed via a config.json file which path is then passed to the bash script when starting the conversion (see §Usage).

## Usage
`mkdir /data/docs_for_conv` (or a different path, then changing the relative _.dataset.path_ value within the config.json file) and add the documents to be converted to the folder. 

```bash start_conversion.sh -c config.json``` or run the script with the `-h` flag to get help with the possible commands.

The chosen folder for the data input will be populated with a directory for each document, containing: the inputted document, a metadata file, a folder for each OCR tool (containing txt files of both the extracted text and the translation to english of such text). 

#### Converted data path structure

    /data/docs_for_conv/
        |
        ├── DocumentName1/
        |   ├── OCRToolName/
        |   |   ├── conversion.txt
        |   |   └── translation.txt
        |   ├── OriginalDocument.pdf
        |   └── metadata.json
        |
        └── DocumentName2/
            ├── ...
