#!/bin/bash

PACKAGE_ROOT=ez_m3u8_creator
SCRIPT_PATH="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
PROJ_MAIN_DIR=$SCRIPT_PATH/../..
pushd "$PROJ_MAIN_DIR"

if [ "$1" == "travis-ci" ]; then
    export PYTEST_ADDOPTS='-m "(not selenium) and (not proxytest)"'
    echo "Argument 'travis-ci' passed, set 'PYTEST_ADDOPTS' env variable"
fi

echo SCRIPT_PATH: $SCRIPT_PATH
echo PROJ_MAIN_DIR: $PROJ_MAIN_DIR
echo PACKAGE_ROOT: $PACKAGE_ROOT

export PYTHONPATH=$PYTHONPATH:$PACKAGE_ROOT

# Can use to overwrite pytest.ini
# set PYTEST_ADDOPTS=""

echo PYTHONPATH: "$PYTHONPATH"

# Test directories are specified in Pytest.ini
pytest --cov="$PACKAGE_ROOT"
return_code=$?

if [[ $return_code -eq  0 ]];
then
    echo "*** No Issues Found"
else
    echo "*** Some Issues Found"
fi

popd
echo "exit $return_code"
exit $return_code
