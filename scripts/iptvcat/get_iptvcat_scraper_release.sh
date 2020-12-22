#!/bin/bash

echo '##### Calling: '`basename "$0"` '('$0')'

### Verify the parsed variables
echo Verifying passed arguments

release_name=$1
dest_dir=$2

if [[ -z ${release_name} ]];
then
    echo "arg1 - Release name is not set"
    exit 1
fi

if [[ -z ${dest_dir} ]];
then
    echo "arg2 - Destination directory is not set"
    exit 1
fi

if [ ! -d ${dest_dir} ] 
then
    echo "Directory '${dest_dir}' DOES NOT exist." 
    exit 1
fi

echo "Release Name '${release_name}'"
echo "Target Dir '${dest_dir}'"

### Download the Release

echo "Command: 'ls -alt ${dest_dir}'"
ls -alt ${dest_dir}

dest_file_path=${dest_dir}/streams.zip

url=https://github.com/eliashussary/iptvcat-scraper/releases/download/$release_name/streams.zip

echo Trying to get release from "$url"
echo "Command: 'curl --fail -L -o ${dest_file_path} $url'"
curl --fail -L -o ${dest_file_path} $url
return_code=$?
if [[ $return_code -ne  0 ]];
then
    echo "*** Some Issues Found downloading the file"
    exit 1
fi

echo "Command: 'ls -alt ${dest_dir}'"
ls -alt ${dest_dir}

### Extract the Release

ignore_files="-x all-*"

echo "Command: 'unzip ${dest_file_path} -d ${dest_dir}' ${ignore_files}"
unzip ${dest_file_path} -d ${dest_dir} ${ignore_files}

echo "Command: 'ls -alt ${dest_dir}'"
ls -alt ${dest_dir}
