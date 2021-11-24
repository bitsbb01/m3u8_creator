#!/bin/bash


### Helper script to merge m3u8 files


#########################################
##### START OF FUNCTION DEFINITIONS #####
#########################################
merge_m3u8_files () {
    local m3u8_merge_into_file=$1
    local m3u8_merge_from_file=$2
    local json_check_file=$3

    echo "### START Processing - '${m3u8_merge_into_file}' ###"

    ls -alt "${m3u8_merge_into_file}"
    ls -alt "${json_check_file}"

    python "${SCRIPT_PATH}/merge_m3u8_files.py" --merge_into_file "${m3u8_merge_into_file}" --merge_from_file "${m3u8_merge_from_file}"

    if [[ $return_code -eq  0 ]];
    then
        echo "   No Issues"
    else
        echo "   Issues Found"
    fi
    echo "### FINISH Processing - '${m3u8_merge_into_file}' ###"
}
#######################################
##### END OF FUNCTION DEFINITIONS #####
#######################################

echo '##### Calling: '`basename "$0"` '('$0')'

### Verify the parsed variables
echo Verifying passed arguments

m3u_merge_into_dir=$1
m3u_merge_from_dir=$2

if [[ -z ${m3u_merge_into_dir} ]];
then
    echo "arg1 - M3u Merge into directory is not set"
    exit 1
fi

if [[ ! -d ${m3u_merge_into_dir} ]];
then
    echo "Directory '${m3u_merge_into_dir}' DOES NOT exist." 
    exit 1
fi

if [[ -z ${m3u_merge_from_dir} ]];
then
    echo "arg1 - M3u Merge from directory is not set"
    exit 1
fi

if [[ ! -d ${m3u_merge_from_dir} ]];
then
    echo "Directory '${m3u_merge_from_dir}' DOES NOT exist." 
    exit 1
fi

### Action ###

SCRIPT_PATH="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

# find "$m3u_merge_into_dir/" "$m3u_merge_from_dir/" -printf '%P\n' | sort | uniq -d
for file in $m3u_merge_into_dir/*.m3u8; do
    name=${file##*/}
    if [[ -f $m3u_merge_from_dir/$name ]]; then
        echo "$name exists in both directories, process"

        merge_m3u8_files "${m3u_merge_into_dir}/${name}" "${m3u_merge_from_dir}/${name}"

    fi
done


