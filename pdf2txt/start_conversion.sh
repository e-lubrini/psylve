#!/bin/bash


## HELP
Help()
{
   # Display Help
   echo "This script starts the conversion pipeline."
   echo
   echo "Syntax: bash script_path [-d|f] [-g]"
   echo
   echo "options:"
   echo "d     Data directory where documents are stored."
   echo "f     A single file to be converted."
   echo "g     Path to the grobid installation."
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
    echo "The script requires at least two arguments. To check the expected syntax, use -h to print Help."
    #exit 1         # TODO: uncomment
fi

# TODO: delete
DIR='data/docs_for_conv/'
GROBID_DIR='../../grobid'


while getopts d:f:g: flag
do
    case "${flag}" in
        d) DIR=${OPTARG};;
        f) FILE=${OPTARG};;
        g) grobid_dir=${OPTARG};;
    esac
done

#echo "directory: $DIR"
#echo "filepath: $FILE"
#echo "gradlew path: $GROBID_DIR"

# start grobid server
#bash './tools/grobid/grobid_server_start.sh' $GROBID_DIR &
#GRO_PID=$! &

# start conversion
(sleep 1; echo 'SLEPT'; python3 'conversion_pipeline.py' $DIR $FILE; pkill -9 $GRO_PID; echo 'KILLED $GRO_PID')