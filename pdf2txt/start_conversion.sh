#!/bin/bash


## HELP
Help()
{
   # Display Help
   echo "This script starts the conversion pipeline."
   echo
   echo "Syntax: bash [path to this script] -c [path to conf]"
   echo
   echo "options:"
   echo "c     Path to the config file."
   echo "f     [OPT] Print additional messages."
   echo
   echo "h     Print this Help."
   echo
}

while getopts ":h" option; do
   case $option in
      h) # display Help
         Help
         exit;;
   esac
done


## CHECK THERE ARE AT LEAST TWO ARGUMENTS
if (( $# < 2 )); then
    echo -e "\033[0;31m The script requires at least one argument. To check the expected syntax, use -h to print Help.\033[0m"
    exit 1
fi

while getopts d:f:g: flag
do
    case "${flag}" in
        c) CONF_FILE=${OPTARG};;
        v) VERBOSE=${OPTARG};;
    esac
done

# start grobid server
databasename=`jq '.grobid_path' $CONF_FILE`
echo '$CONF_FILE'
#bash './tools/grobid/grobid_server_start.sh' $GROBID_DIR &
#GRO_PID=$! &

# start conversion
(sleep 1; echo 'SLEPT'; python3 'conversion_pipeline.py' $CONF_FILE; pkill -9 $GRO_PID; echo 'KILLED $GRO_PID')