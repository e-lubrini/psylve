<h1 align="center">PsylVe</h1>
<h2 align="center">An Ontology of Psyllids as Vectors of Phytoplasma</h2>

Ontology Development project @ CIRAD, and INRAE for an ontology of superfamily Psylloidea with a focus on its role as vecor of phythoplasma.

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


## Modules
- Text extraction [README](https://github.com/e-lubrini/PsylVe/blob/main/pdf2txt/README.md)
