<h1 align="center">Dataset Overview</h1>
This module analyses the composition of the dataset and the relationships between attributes.

## Directory Tree

    dataset_overview/
        ├── imgs/
        ├── tools/
        ├── dataset_metadata.csv
        ├── fca.ipynb
        └── dataset_visualisations.ipynb
        

## Formal Concept Analysis (FCA)
The first notebook in this module, a formal concept analysis (FCA) was carried out in order to find the attributes within the dataset that showed the highest correlation.


<div style="text-align:center" align="center"><img width="450" src=path /></div>

HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH

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
- Configuration settings can be changed via a ``config.json`` file which path is then passed to the ``start_conversion.sh`` bash script when launching the conversion (see [§ Usage](#usage)).

- The configuration file allows you to choose a list of tools for text extraction. For more information on which tools work best for your chosen documents, place them in a ``/data/docs_for_extr`` folder, open the ``evaluation_pipeline.ipynb`` notebook, and run it to see a visual representation of each tool's performance. More tools and evaluation scores can be easily added (see [§ Adding More Features](adding-more-features))

## Usage
- `mkdir /data/docs_for_conv` (or a different path, then changing the relative _.dataset.path_ value within the ``config.json`` file) and add the documents to be converted to the folder. 

- ```bash start_conversion.sh -c config.json``` or run the script with the `-h` flag to get help with the possible commands.

- The chosen folder for the data input will be populated with a directory for each document, containing:
    - the inputted document,
    - a metadata file,
    - a folder for each OCR tool (containing `txt` files of both the extracted text and the translation to english of such text). 

#### Converted data path structure

    /data/docs_for_extr/
        |
        ├── DocumentName1/
        |   ├── OCRToolName/
        |   |   ├── ocr_extraction.txt
        |   |   └── translation.txt
        |   |
        |   ├── grobid/
        |   |   ├── emb_xml.txt
        |   |   └── translation.txt
        |   |
        |   ├── OriginalDocument.pdf
        |   └── metadata.json
        |
        └── DocumentName2/
            ├── ...
    
    
    /data/final_files/
        |
        ├── DocumentName1.txt
        ├── DocumentName1.txt
        |   ...
        |
        └── metadata.csv

## Adding More Features
- New **tools for conversion** can be easily added to ``tools/conv_tools.py`` by importing the required packages and defining a new function. The function name will then need to be added to the config file, in order for it to be used for conversion, or to the config section in the ``evaluation_pipeline.ipynb`` notebook, in order to evaluate it.

    <h4>format</h4>

    ```python
        def toolname_ocr(pdf_filepath: str):
            ...
            return text         # string
    ```

- More **scores for evaluation** can also be added, by creating a new function in ``tools/eval_tools.py`` and adding it to the congiguration section in the ``evaluation_pipeline.ipynb`` notebook.

    <h4>format</h4>

    ```python
        def evaluation_name(conv_txt: str,           # converted text to be evaluated
                            lang_codes: str,         # two-letter code representing language of the original documant
                            max_words_per_doc: int,  # max number of words to be used for evaluation
                            ): 
            ...
            return score    # int; 0 ≤ score ≤ 1
    ```

## Legend: Configuration Options 

<h4>general</h4>

- `overwrite` / `store_output` — true/false values; whether to store the following data and overwrite it if existing 
    - `lang_codes` — (metadata) the 2-letter code of the language of the document
    - `emb_txt` — (metadata) the text embedded in the document
    - `emb_txt_trans` — (metadata) the translation of the embedded text to English
    - `emb_xml` — (directory) the embedded text in xml form, outlining the document layout
    - `emb_xml_trans` — (directory) the translation of the xml to English
    - `ocr_txt` — (directory) text extracted with the selected OCR tool
    - `ocr_txt_trans` — (directory) the translation of text extracted with the selected OCR tool to English
    - `emb_txt_ok` — (metadata) whether the embedded text has good quality, depending on a threshold - set below

<h4>dataset</h4>

- `path` — the path of the directory containing the documents to be processed

<h4>conversion</h4>

- `tool_names` — the names of the tools to be used for conversion (can be chosen based on results in the evaluation pipeline notebook)
- `convert_if_emb_txt_ok` — convert even if the embedded text has good quality
- `emb_txt_ok_threshold` — threshold to label embedded text as good quality
    
<h4>grobid</h4>

- `grobid_inst_path` — path to the grobid installation
- `config_path` — path to the configuration file for grobid
- `GROBID_URL` — 
- `end_url` — 

<h4>appearance</h4>

- `message_colours` — colours of the messages to be displayed
