
<p align="center">
  <img src="http://some_place.com/image.png](https://github.com/e-lubrini/psylve/blob/main/img/logos/logo_g.png" />
</p>

<h2 align="center">An Ontology of Psyllids as Vectors of Phytoplasma</h2>

Ontology Development project @ INRAE for an ontology of superfamily Psylloidea with a focus on its role as vecor of phythoplasma.

## Modules
- Dataset Overview [README](https://github.com/e-lubrini/PsylVe/blob/main/dataset_overview/README.md)
- Text Extraction [README](https://github.com/e-lubrini/PsylVe/blob/main/text_extraction/README.md)
- Ner Correction [README](https://github.com/e-lubrini/PsylVe/blob/main/ner_correction/README.md)

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
