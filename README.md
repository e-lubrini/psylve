
<p align="center">
  <img src="https://github.com/e-lubrini/psylve/blob/main/data/imgs/logos/logo_g.png" width="250" />
</p>

<h2 align="center">A Text-to-Ontology Information
Extraction Framework<br>for the Occurrence
Distribution of Plant Pathogen Vectors</h2>

Ontology and Text Mining project @ INRAE optimised on data concerning the taxonomic superfamily Psylloidea with a focus on its role as vecor of phythoplasma.

## Pipeline Modules
- Dataset Overview [README](https://github.com/e-lubrini/psylve/tree/main/src/data_overview)
- Text Extraction [README](https://github.com/e-lubrini/psylve/tree/main/src/text-extraction)
- Ontology [README](https://github.com/e-lubrini/psylve/tree/main/src/ontology)
- NER [README](https://github.com/e-lubrini/psylve/tree/main/src/ner)
- Evaluation [README](https://github.com/e-lubrini/psylve/tree/main/src/evaluation)

## Code Structure Overview
Main files in the pipeline. To see the directory tree in more detail, check the README of the modules above.
  
    src/
    ├── dataset_overview/
    |   ├── dataset_metadata.csv  # metadata of documents composing the dataset
    |   └── dataset_visualisation.ipynb 
    |
    ├── text_extraction/
    |   ├── data/  # documents composing the dataset
    |   └── launch.sh
    |
    ├── ontology/
    |   ├── ontology.ipynb
    |   └── ontology.ttl
    |
    ├── ner/
    |   ├── data/  # preprocessed documents (text extracted and translated)
    |   └── launch.sh
    |
    └── evaluation/
         ├── data/  # labels and predictions          
         └── launch.sh

## Usage
The `dataset_overview` module includes a notebook with an overview of the dataset. The modules `text_extraction`, `ner_correction`, and `evaluation` have each their own bash script that can be run via `cd src/[NAME_OF_MODULE]; bash launch.sh [ARGUMENTS]`. The `ontology` module contains a `.ttl` ontology and a Python notebook for its visualisation.

#### [▲ Back to top](https://github.com/e-lubrini/psylve/tree/internship#a-text-to-ontology-informationextraction-frameworkfor-the-occurrencedistribution-of-plant-pathogen-vectors)
