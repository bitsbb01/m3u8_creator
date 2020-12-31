#!/bin/bash

echo '##### Calling: '`basename "$0"` '('$0')'

### Verify the parsed variables
echo Verifying passed arguments

file_url=$1
dest_dir=$2
dest_filename=$3


if [[ -z ${file_url} ]];
then
    echo "arg1 - Url is not set"
    exit 1
fi

if [[ -z ${dest_dir} ]];
then
    echo "arg2 - Destination directory is not set"
    exit 1
fi

if [[ ! -d ${dest_dir} ]];
then
    echo "Directory '${dest_dir}' DOES NOT exist." 
    exit 1
fi

if [[ -z ${dest_filename} ]];
then
    echo "arg2 - Destination Filename is not set"
    exit 1
fi

### Download the Release

echo "Command: 'ls -alt ${dest_dir}'"
ls -alt ${dest_dir}

dest_file_path=${dest_dir}/${dest_filename}

echo Trying to get file from "$url"
echo "Command: 'curl --fail -L -o "${dest_file_path}" ${file_url}'"
curl --fail -L -o "${dest_file_path}" ${file_url}
return_code=$?
if [[ $return_code -ne  0 ]];
then
    echo "*** Some Issues Found downloading the file"
    exit 1
fi

echo "Command: 'ls -alt "${dest_file_path}"'"
ls -alt "${dest_file_path}"
