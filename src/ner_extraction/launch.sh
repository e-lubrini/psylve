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
            p)  
                DB_FILE_PATH=${OPTARG}
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


cd ../../../text-mining-workflow/
bash batch-process.sh -p $DB_PATH
