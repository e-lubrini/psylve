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
    

WF_PATH="../../../text-mining-workflow/"
REL_PWD="../../../../psylve/src/ner_extraction/"
cd $WF_PATH
FULL_DB_PATH="$REL_PWD$DB_PATH"
echo "hi $FULL_DB_PATH"
bash batch-process.sh $FULL_DB_PATH