#!/bin/bash

## HELP
Help()
{  # Display Help
   echo "This script starts the conversion pipeline."
   echo
   echo "Syntax: bash $(basename \$0) [-c] [-v] [-t]"
   echo
   echo "options:"
   echo "d    Path to the document database."
   echo "v     [OPT] Print additional messages."
   echo "t     [OPT] Print time messages."
   echo
   echo "h     Print this Help message."
   echo
}


## ARGUMENTS
while getopts 'hd:vt' flag
    do
        case "${flag}" in
            h)  # display Help
                Help
                exit
                ;;
            d)  
                DB_PATH=${OPTARG}
                echo 'database path is' $DB_PATH
                ;;
            v)
                VERBOSE='-v'
                ;;
            t)
                TIME_VERB='-t'
                ;;
        esac
    done

#python $EVAL_DIR"/compare_label-prediction.py" $EVAL_DIR"/"$LABEL_FILE #$PREDICTION_FILE
#python $EVAL_DIR"/scores_and_visuals.py"

EVAL_DIR=data/output/
REL_PWD=../../../../psylve/src/ner_extraction/
echo "$REL_PWD$EVAL_DIR"
cd ../../../text-mining-workflow/
bash batch-process.sh "$REL_PWD$DB_PATH"
