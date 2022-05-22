#!/bin/bash

## HELP
Help()
{  # Display Help
   echo "This script starts the conversion pipeline."
   echo
   echo "Syntax: bash $(basename \$0) [-v] [-c]"
   echo
   echo "options:"
   echo "c     Path to the config file."
   echo "v     [OPT] Print additional messages."
   echo
   echo "h     Print this Help."
   echo
}


## COMMAND IS VALID
if (( $# < 1 )); then
    echo -e "\033[0;31m The script requires at least one argument. To check the expected syntax, use -h to print Help.\033[0m"
    exit 1
fi


## ARGUMENTS
while getopts 'hc:v' flag
    do
        case "${flag}" in
            h)  # display Help
                Help
                exit
                ;;
            c)  
                CONF_FILE_PATH=${OPTARG}
                echo 'conf file is' $CONF_FILE_PATH
                ;;
            v)
                VERBOSE='verbose'
                echo 'verbose is' $VERBOSE
                ;;
        esac
    done


## FUNCTIONS
StartGrobidServer()
{   # Start grobid server
    cd $GPATH;
    bash ./gradlew run > /dev/null
}

KillGrobid()
{   # Kill all grobid processes 
    for p in `ps -aux | grep grobid | awk -F ' ' '{print $2}' `; do
        echo 'KILLING' $p '...'
        kill -9 $p
    done
}


## PIPELINE
GPATH=($(jq -r '.grobid.grobid_inst_path' $CONF_FILE_PATH))
#StartGrobidServer & 
(   # start conversion
    sleep 1;
    python 'conversion_pipeline.py' $CONF_FILE_PATH $VERBOSE;
    KillGrobid;
    echo 'Pipeline exited successfully.';
    exit
)
