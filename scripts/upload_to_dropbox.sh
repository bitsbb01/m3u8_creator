#!/bin/bash

echo '##### Calling: '`basename "$0"` '('$0')'

### Verify the parsed variables
echo Verifying passed arguments

upload_dir=$1
dropbox_dir=$2
dropbox_token=$3

if [[ -z ${upload_dir} ]];
then
    echo "arg1 - Upload directory is not specifies"
    exit 1
fi

if [[ -z ${dropbox_dir} ]];
then
    echo "arg2 - Dropbox directory is not specifies"
    exit 1
fi

if [[ -z ${dropbox_token} ]];
then
    echo "arg3 - Dropbox Token is not specifies"
    exit 1
fi

if [[ ! -d ${upload_dir} ]];
then
    echo "Directory '${upload_dir}' DOES NOT exist." 
    exit 1
fi

echo "Upload directory '${upload_dir}'"


### Upload the files

pushd "${upload_dir}"
for filename in *; do
  if [ -f "${filename}" ]; then  # Only Files
    echo "COMMAND curl --fail -X POST https://content.dropboxapi.com/2/files/upload \
        --header "Authorization: Bearer **********" \
        --header "Dropbox-API-Arg: {\"path\": \"/${dropbox_dir}/${filename}\", \"mode\": \"overwrite\"}" \
        --header "Content-Type: application/octet-stream" \
        --data-binary @"${filename}""

    curl --fail -X POST https://content.dropboxapi.com/2/files/upload \
        --header "Authorization: Bearer ${dropbox_token}" \
        --header "Dropbox-API-Arg: {\"path\": \"/${dropbox_dir}/${filename}\", \"mode\": \"overwrite\"}" \
        --header "Content-Type: application/octet-stream" \
        --data-binary @"${filename}"
    return_code=$?
    echo "*** Return Code: ${return_code}"
    if [[ ${return_code} -ne  0 ]];
    then
        echo "*** Error Code: ${return_code} - Some Issues Found uploading '${filename}'"
        exit 1
    fi
  fi
done
popd
