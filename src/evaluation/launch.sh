#!/bin/bash

## HELP
Help()
{  # Display Help
   echo "This script starts the conversion pipeline."
   echo
   echo "Syntax: bash $(basename \$0) [-c] [-v] [-t]"
   echo
   echo "options:"
   echo "p     Path to the document database."
   echo "v     [OPT] Print additional messages."
   echo "t     [OPT] Print time messages."
   echo
   echo "h     Print this Help message."
   echo
}


## ARGUMENTS
while getopts 'hpl:vt' flag
    do
        case "${flag}" in
            h)  # display Help
                Help
                exit
                ;;
            p)  
                EVAL_PATH=${OPTARG}
                echo 'database path is' $EVAL_PATH
                ;;
            l)  
                LABEL_FILE=${OPTARG}
                echo 'label path is' $LABEL_FILE
                ;;
            v)
                VERBOSE='-v'
                ;;
            t)
                TIME_VERB='-t'
                ;;
        esac
    done


python compare_label-prediction.py $LABEL_FILE #$PREDICTION_FILE
python scores_and_visuals.py
