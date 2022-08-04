
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

## Repository Structure

    dataset_overview/
        ├── imgs/
        ├── tools/
        ├── dataset_metadata.csv
        ├── fca.ipynb
        └── dataset_visualisations.ipynb
        
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
        
    ner_correction/
        ├── tools/
        ├── analysis/
        |   ├── data/
        |   └── ner_correction_overview.ipynb
        └── correction_modules/
