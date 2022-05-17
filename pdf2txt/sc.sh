#!/bin/bash

## HELP
Help()
{  # Display Help
   echo "This script starts the conversion pipeline."
   echo
   echo "Syntax: bash $(basename \$0) [-c]"
   echo
   echo "options:"
   echo "c     Path to the config file."
   echo "f     [OPT] Print additional messages."
   echo
   echo "h     Print this Help."
   echo
}
while getopts ":h" OPTION
do
   case $OPTION in
      h) # display Help
         Help
         exit;;
   esac
done

## CHECK THERE ARE AT LEAST TWO ARGUMENTS
if (( $# < 1 )); then
    echo -e "\033[0;31m The script requires at least one argument. To check the expected syntax, use -h to print Help.\033[0m"
    exit 1
fi

## ARGUMENTS
while getopts 'c:v' OPTION
do
    case $OPTION in
        c)  
            CFP=${OPTARG}
            echo 'conf file is $CONF_FILE_PATH'
            ;;
        v)
            VERBOSE='$true'
            ;;
    esac
done