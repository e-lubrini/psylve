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
while getopts 'hc:vt' flag
    do
        case "${flag}" in
            h)  # display Help
                Help
                exit
                ;;
            l)  
                LABEL_FILE=${OPTARG}
                echo 'database path is' $LABEL_FILE
                ;;
            p)  
                PREDICTION_FILE=${OPTARG}
                echo 'database path is' $PREDICTION_FILE
                ;;
            v)
                VERBOSE='-v'
                ;;
            t)
                TIME_VERB='-t'
                ;;
        esac
    done


cd ../../../text-mining-workflow/
python compare_label-prediction.py.sh $LABEL_FILE $PREDICTION_FILE
