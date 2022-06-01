<h1 align="center">Text Extraction</h1>
<div style="text-align:center" align="center"><img width="450" src=https://github.com/e-lubrini/psylloidea_ontology/blob/main/text_extraction.drawio.png /></div>

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

- **Install Python packages —**
```cat pip_requirements.txt | xargs -n 1 pip install```
This pipeline requires a Python version of at least 3.10.

- **Install APT packages —**
```sed 's/#.*//' apt_requirements.txt | xargs sudo apt-get install```

- **Clone required GitHub repositories —**
`cd tools` (or a different path, then changing the relative _.grobid.config_path_ value within the config.json file) and install _grobid_client_python_ by following the [instructions](https://github.com/kermitt2/grobid_client_python)
```
git clone https://github.com/kermitt2/grobid_client_python
cd grobid_client_python
python3 setup.py install
```
## Configuration and Tool Selection
- Configuration settings can be changed via a ``config.json`` file which path is then passed to the ``start_conversion.sh`` bash script when launching the conversion (see § Usage).

- The configuration file allows you to choose a list of tools for text extraction. For more information on which tools work best for your chosen docun
ments, place them in a ``/data/docs_for_conv`` folder, open the ``evaluation_pipeline.ipynb`` notebook, and run it to see a visual representation of each tool's performance. More tools and evaluation scores can be easily added (see § Adding More Features)

## Usage
- `mkdir /data/docs_for_conv` (or a different path, then changing the relative _.dataset.path_ value within the ``config.json`` file) and add the documents to be converted to the folder. 

- ```bash start_conversion.sh -c config.json``` or run the script with the `-h` flag to get help with the possible commands.

- The chosen folder for the data input will be populated with a directory for each document, containing: the inputted document, a metadata file, a folder for each OCR tool (containing txt files of both the extracted text and the translation to english of such text). 

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

## Adding More Features
- New **tools for conversion** can be easily added to ``tools/conv_tools.py`` by importing the required packages and defining a new function. The function name will then need to be added to the config file, in order for it to be used for conversion, or to the config section in the ``evaluation_pipeline.ipynb`` notebook, in order to evaluate it.

- More **scores for evaluation** can also be added, by creating a new function in ``tools/eval_tools.py`` and adding it to the congiguration section in the ``evaluation_pipeline.ipynb`` notebook.

## Configuration Options

#### general

- overwrite:
    - lang_codes": false,
    - emb_txt": false,
    - emb_txt_trans": false,
    - emb_xml": false,
    - emb_xml_trans": false,
    - ocr_txt": false,
    - ocr_txt_trans": false,
    - emb_txt_ok": false
    
- store_output
    - lang_codes": true,
    - emb_txt": true,
    - emb_txt_trans": false,
    - emb_xml": true,
    - emb_xml_trans": false,
    - ocr_txt": true,
    - ocr_txt_trans": true,
    - emb_txt_ok": true

#### dataset

- path: /home/elubrini/GitHub/psylve/pdf2txt/data/docs_for_conv
- path: /home/elubrini/GitHub/psylve/pdf2txt/data/test

#### conversion

- tool_names
- convert_if_emb_txt_ok
- emb_txt_ok_threshold 
    
#### grobid

- grobid_inst_path
- config_path
- GROBID_URL
- end_url

#### appearance

- message_colours
