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


## CHECK THERE IS AT LEAST ONE ARGUMENT
if (( $# < 1 )); then
    echo -e "\033[0;31m The script requires at least one argument. To check the expected syntax, use -h to print Help.\033[0m"
    exit 1
fi


## ARGUMENTS
while getopts 'hc:v' flag
    do
        case "${flag}" in
            h) # display Help
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

# start grobid server
#bash './tools/grobid/grobid_server_start.sh' $CONF_FILE_PATH $VERBOSE &
#GRO_PID=$! &
# start conversion
(sleep 1;
echo 'SLEPT'; python3 'conversion_pipeline.py' $CONF_FILE_PATH $VERBOSE;
pkill -9 $GRO_PID;
echo 'KILLED $GRO_PID')
