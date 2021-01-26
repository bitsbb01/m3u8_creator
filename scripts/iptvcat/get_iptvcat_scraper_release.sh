#!/bin/bash

echo '##### Calling: '`basename "$0"` '('$0')'

### Verify the parsed variables
echo Verifying passed arguments

dest_dir=$1
release_name_1=$2
release_name_2=$3

if [[ -z ${dest_dir} ]];
then
    echo "arg1 - Destination directory is not set"
    exit 1
fi

if [[ ! -d ${dest_dir} ]];
then
    echo "Directory '${dest_dir}' DOES NOT exist." 
    exit 1
fi

if [[ -z ${release_name_1} ]];
then
    echo "arg2 - Release name 1 is not set"
    exit 1
fi

if [[ -z ${release_name_2} ]];
then
    echo "arg3 - Release name 2 is not set"
    exit 1
fi

echo "Target Dir '${dest_dir}'"
echo "Release Name 1'${release_name_1}'"
echo "Release Name 2'${release_name_2}'"

### Download the Release
release_name_list=()
release_name_list+=(${release_name_1})
release_name_list+=(${release_name_2})

for param in ${release_name_list[@]}; do

    echo "Command: 'ls -alt ${dest_dir}'"
    ls -alt ${dest_dir}

    dest_file_path=${dest_dir}/streams.zip

    url=https://github.com/eliashussary/iptvcat-scraper/releases/download/${param}/streams.zip

    echo Trying to get release from "$url"
    echo "Command: 'curl --fail -L -o ${dest_file_path} $url'"
    curl --fail -L -o ${dest_file_path} $url
    return_code=$?

    if [[ -f ${dest_file_path} ]];
    then
        echo "File Found for release ${param}"
        break
    fi
done

if [[ ! -f ${dest_file_path} ]];
then
    echo "No File Found for any release"
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
