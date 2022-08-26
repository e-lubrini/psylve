<h1 align="center">NER Corrections</h1>

This module contains:
- an analysis of the issues found during the application of the AlvisNLP NER tool on the PsylVe dataset;
- Improvements and contributions to the AlvisNLP tool.

## Directory Structure

    ner_correction/
        ├── tools/
        ├── analysis/
        |   ├── data/
        |   └── ner_correction_overview.ipynb
        ├── correction_modules/
        └── launch.sh

## Usage
`cd` to `psylve/src/ner_extraction/` directory and run the `launch.sh` script followed by a `-d` flag with the path to the text database for named entities to be extracted. The text documents must be in a child folder called `txt`.

### Example
#### file structure
      src/
        ├── text_extraction/
        |   └── data/
        |       └── txt/
        |           ├── doc_1.txt
        |           ├── doc_2.txt
        |           ├── doc_3.txt
        |           └── ...
        |
        ├── ner_correction/
        |   └── launch.sh
        ...

#### command
```bash
cd psylve/src/ner_extraction
bash launch.sh -d ../text_extraction/data/
```
## Modules
- Correction Modules [README](https://github.com/e-lubrini/PsylVe/blob/main/dataset_overview/README.md)


#### [◄ Back to main README](https://github.com/e-lubrini/PsylVe/blob/main/README.md)