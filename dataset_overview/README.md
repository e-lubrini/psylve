<h1 align="center">Dataset Overview</h1>
This module analyses the composition of the dataset and the relationships between attributes.

## Directory Tree

    dataset_overview/
        ├── imgs/
        ├── tools/
        ├── dataset_metadata.csv        # metadata of all documents in corpus
        ├── fca.ipynb       # carries out FCA and visualisation; saves output figures
        └── dataset_visualisations.ipynb        # visualises corpus; saves output figures
        

## Formal Concept Analysis (FCA)
The first notebook in this module, a formal concept analysis (FCA) was carried out in order to find the attributes within the dataset that showed the highest correlation. Visualisations are produced automatically mapping each couple of highly correlated attributes (y axis and colour code) onto the only ordinal attribute, i.e. date of the document (x axis).

Here is an automatically generated example plotting one of the most correlated combinations: date vs language grouped by database:


<div style="text-align:center" align="center"><img width="450" src=https://github.com/e-lubrini/psylve/blob/main/dataset_overview/imgs/fca/dateidentified_vs_language_grouped_by_availability.png /></div>



#### [◄ Back to main README](https://github.com/e-lubrini/PsylVe/blob/main/README.md)

