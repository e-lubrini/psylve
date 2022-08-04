<h1 align="center">Dataset Overview</h1>
This module analyses the composition of the dataset and the relationships between attributes and provides some visualisations for a quiccker understanding of its composition.

## Directory Tree

    dataset_overview/
        ├── imgs/
        ├── tools/
        ├── dataset_metadata.csv        # metadata of all documents in corpus
        ├── fca.ipynb       # carries out FCA and visualisation; saves output figures
        └── dataset_visualisations.ipynb        # visualises corpus; saves output figures
        

## Formal Concept Analysis (FCA)
The first notebook in this module, a formal concept analysis (FCA) was carried out in order to find the attributes within the dataset that showed the highest correlation. Visualisations are produced automatically mapping each couple of highly correlated attributes (y axis and colour code) onto the only ordinal attribute, i.e. date of the document (x axis).

Here is an automatically generated example plotting one of the most correlated combinations:

<h4 align="center">date vs language grouped by availability</h4>

<div style="text-align:center" align="center"><img width="450" src=https://github.com/e-lubrini/PsylVe/blob/main/src/dataset_overview/imgs/fca/dateidentified_vs_language_grouped_by_availability.png /></div>


## Visualisations
The FCA Analysis helped navigating the most interesting correlation, from which more plots were manually generated.
All the plots can be found in the [imgs](https://github.com/e-lubrini/PsylVe/blob/main/src/dataset_overview/imgs) folder, and the code in the respective nottebooks [dataset_visualisation.ipynb](https://github.com/e-lubrini/PsylVe/blob/main/src/dataset_overview/dataset_visualisation.ipynb) and [fca.ipynb](https://github.com/e-lubrini/PsylVe/blob/main/src/dataset_overview/fca.ipynb).
Following are a few examples:

<h4 align="center">date vs database grouped by language</h4>

<div style="text-align:center" align="center"><img width="450" src=https://github.com/e-lubrini/PsylVe/blob/main/src/dataset_overview/imgs/date_vs_database_grouped_by_language.png /></div>

<h4 align="center">date vs accessibility grouped by language</h4>

<div style="text-align:center" align="center"><img width="450" src=https://github.com/e-lubrini/PsylVe/blob/main/src/dataset_overview/imgs/date_vs_accessibility_grouped_by_language.png /></div>



#### [◄ Back to main README](https://github.com/e-lubrini/PsylVe/blob/main/README.md)

