#!/bin/bash

echo '##### Calling: '`basename "$0"` '('$0')'

#########################################
##### START OF FUNCTION DEFINITIONS #####
#########################################
run_tester () {
    local tester_name=$1
    local tester_script=$2

    echo "### TESTING START - '$tester_script' ###"
    "$tester_script"
    local return_code=$?

    if [[ $return_code -eq  0 ]];
    then
        echo "   No Issues"
    else
        echo "   Issues Found"
        ERROR_FOUND="true"
        ERROR_LIST+=" $tester_name"
    fi
    echo "### TESTING END - '$tester_name' ###"
}
#######################################
##### END OF FUNCTION DEFINITIONS #####
#######################################

SCRIPT_PATH="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
TEST_DIR=$SCRIPT_PATH/Testing

echo SCRIPT_PATH: $SCRIPT_PATH
echo TEST_DIR: $TEST_DIR

ERROR_FOUND="false"
ERROR_LIST=''

echo "### Start Testing ###"
run_tester "Pytest"         "$TEST_DIR/RunPytest.sh"
echo "### Testing finished ###"

echo "ERROR_FOUND: '$ERROR_FOUND'"
if [ $ERROR_FOUND == "false" ];
then
    echo "!!! NO TESTING ISSUE FOUND"
    echo "exit 0"
    exit 0
else
    echo "!!! CHECK OUTPUT, SOME TESTING ISSUE FOUND WITH"
    for value in $ERROR_LIST
    do
        echo "  - $value"
    done
    echo "exit 1"
    exit 1
fi
