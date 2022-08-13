
<p align="center">
  <img src="https://github.com/e-lubrini/psylve/blob/main/img/logos/logo_g.png" width="250" />
</p>

<h2 align="center">A Text-to-Ontology Information
Extraction Tool<br>for the Occurrence
Distribution of Plant Pathogen Vectors</h2>

Ontology and Text Mining project @ INRAE optimised on data concerning the taxonomic superfamily Psylloidea with a focus on its role as vecor of phythoplasma.

## Modules
- Dataset Overview [README](https://github.com/e-lubrini/PsylVe/blob/main/src/dataset_overview/README.md)
- Text Extraction [README](https://github.com/e-lubrini/PsylVe/blob/main/src/text_extraction/README.md)
- Ner Correction [README](https://github.com/e-lubrini/PsylVe/blob/main/src/ner_correction/README.md)
- Ontology [README](https://github.com/e-lubrini/psylve/tree/main/src/ontology/README.md)
- Evaluation [README](https://github.com/e-lubrini/psylve/tree/main//srcevaluation/README.md)

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
    |   └── psylve.ttl
    |
    ├── ner_correction/
    |   ├── data/  # preprocessed documents (text extracted and translated)
    |   └── launch.sh
    |
    └── evaluation/
         ├── data/  # labels and predictions          
         └── launch.sh
