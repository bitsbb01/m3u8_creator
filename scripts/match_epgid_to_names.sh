#!/bin/bash


### FOR NOW UST A HELPER SCRIPT WITH HARDCODED WITH IDS WE'RE LOOKING UP
### IN THE FUTURE WE WANT TO FIND A MORE GENERIC WAY


#########################################
##### START OF FUNCTION DEFINITIONS #####
#########################################
match_epg_id_for_file () {
    local m3u8_in_file=$1
    local m3u8_out_file=$2
    local json_check_file=$3

    echo "### START Processing - '${m3u8_in_file}' ###"

    ls -alt "${m3u8_in_file}"
    ls -alt "${json_check_file}"

    python "${SCRIPT_PATH}/match_epgid_to_names.py" --input_file "${m3u8_in_file}" --out_file "${m3u8_out_file}" --json_file "${json_check_file}"

    if [[ $return_code -eq  0 ]];
    then
        echo "   No Issues"
    else
        echo "   Issues Found"
    fi
    echo "### FINISH Processing - '${m3u8_in_file}' ###"
}
#######################################
##### END OF FUNCTION DEFINITIONS #####
#######################################

echo '##### Calling: '`basename "$0"` '('$0')'

### Verify the parsed variables
echo Verifying passed arguments

m3u_in_dir=$1
m3u_out_dir=$2

if [[ -z ${m3u_in_dir} ]];
then
    echo "arg1 - M3u input directory is not set"
    exit 1
fi

if [[ ! -d ${m3u_in_dir} ]];
then
    echo "Directory '${m3u_in_dir}' DOES NOT exist." 
    exit 1
fi

if [[ -z ${m3u_out_dir} ]];
then
    echo "arg1 - M3u output directory is not set"
    exit 1
fi

if [[ ! -d ${m3u_out_dir} ]];
then
    echo "Directory '${m3u_out_dir}' DOES NOT exist." 
    exit 1
fi

### Action ###

SCRIPT_PATH="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
json_dir=${SCRIPT_PATH}/../ez_m3u8_creator/m3u4u.com/egp-channel-ids

echo SCRIPT_PATH: ${SCRIPT_PATH}
echo Command: 'ls -alt "${m3u_in_dir}"'
ls -alt "${m3u_in_dir}"
echo Command: 'ls -alt "${m3u_out_dir}"'
ls -alt "${m3u_out_dir}"
echo Command: 'ls -alt "${json_dir}"'
ls -alt "${json_dir}"

# Match the known json files
match_epg_id_for_file "${m3u_in_dir}/canada.m3u8" "${m3u_out_dir}/canada.m3u8" "${json_dir}/canada.json"
match_epg_id_for_file "${m3u_in_dir}/canada.m3u8" "${m3u_out_dir}/canada.m3u8" "${json_dir}/canada2.json"
match_epg_id_for_file "${m3u_in_dir}/canada.m3u8" "${m3u_out_dir}/canada.m3u8" "${json_dir}/canada3.json"

match_epg_id_for_file "${m3u_in_dir}/uk-streams.m3u8" "${m3u_out_dir}/uk-streams.m3u8" "${json_dir}/UnitedKingdom.json"
match_epg_id_for_file "${m3u_in_dir}/uk-streams.m3u8" "${m3u_out_dir}/uk-streams.m3u8" "${json_dir}/UnitedKingdom2.json"
match_epg_id_for_file "${m3u_in_dir}/uk-streams.m3u8" "${m3u_out_dir}/uk-streams.m3u8" "${json_dir}/UnitedKingdom3.json"

match_epg_id_for_file "${m3u_in_dir}/catusa.m3u8" "${m3u_out_dir}/catusa.m3u8" "${json_dir}/USA.json"
match_epg_id_for_file "${m3u_in_dir}/catusa.m3u8" "${m3u_out_dir}/catusa.m3u8" "${json_dir}/USA2.json"
match_epg_id_for_file "${m3u_in_dir}/catusa.m3u8" "${m3u_out_dir}/catusa.m3u8" "${json_dir}/USA3.json"
match_epg_id_for_file "${m3u_in_dir}/catusa.m3u8" "${m3u_out_dir}/catusa.m3u8" "${json_dir}/USA4.json"
match_epg_id_for_file "${m3u_in_dir}/catusa.m3u8" "${m3u_out_dir}/catusa.m3u8" "${json_dir}/USA5.json"
match_epg_id_for_file "${m3u_in_dir}/catusa.m3u8" "${m3u_out_dir}/catusa.m3u8" "${json_dir}/USA6.json"
match_epg_id_for_file "${m3u_in_dir}/catusa.m3u8" "${m3u_out_dir}/catusa.m3u8" "${json_dir}/USA7.json"
match_epg_id_for_file "${m3u_in_dir}/catusa.m3u8" "${m3u_out_dir}/catusa.m3u8" "${json_dir}/USA8.json"
match_epg_id_for_file "${m3u_in_dir}/catusa.m3u8" "${m3u_out_dir}/catusa.m3u8" "${json_dir}/USA9.json"
match_epg_id_for_file "${m3u_in_dir}/catusa.m3u8" "${m3u_out_dir}/catusa.m3u8" "${json_dir}/USA10.json"
match_epg_id_for_file "${m3u_in_dir}/catusa.m3u8" "${m3u_out_dir}/catusa.m3u8" "${json_dir}/USA11.json"
match_epg_id_for_file "${m3u_in_dir}/catusa.m3u8" "${m3u_out_dir}/catusa.m3u8" "${json_dir}/USA12.json"
match_epg_id_for_file "${m3u_in_dir}/catusa.m3u8" "${m3u_out_dir}/catusa.m3u8" "${json_dir}/USA13.json"
match_epg_id_for_file "${m3u_in_dir}/catusa.m3u8" "${m3u_out_dir}/catusa.m3u8" "${json_dir}/USA14.json"
match_epg_id_for_file "${m3u_in_dir}/catusa.m3u8" "${m3u_out_dir}/catusa.m3u8" "${json_dir}/USA15.json"
match_epg_id_for_file "${m3u_in_dir}/catusa.m3u8" "${m3u_out_dir}/catusa.m3u8" "${json_dir}/USA16.json"
match_epg_id_for_file "${m3u_in_dir}/catusa.m3u8" "${m3u_out_dir}/catusa.m3u8" "${json_dir}/USA17.json"


match_epg_id_for_file "${m3u_in_dir}/cxtvlive.m3u8" "${m3u_out_dir}/cxtvlive.m3u8" "${json_dir}/USA.json"
match_epg_id_for_file "${m3u_in_dir}/cxtvlive.m3u8" "${m3u_out_dir}/cxtvlive.m3u8" "${json_dir}/USA2.json"
match_epg_id_for_file "${m3u_in_dir}/cxtvlive.m3u8" "${m3u_out_dir}/cxtvlive.m3u8" "${json_dir}/USA3.json"
match_epg_id_for_file "${m3u_in_dir}/cxtvlive.m3u8" "${m3u_out_dir}/cxtvlive.m3u8" "${json_dir}/USA4.json"
match_epg_id_for_file "${m3u_in_dir}/cxtvlive.m3u8" "${m3u_out_dir}/cxtvlive.m3u8" "${json_dir}/USA5.json"
match_epg_id_for_file "${m3u_in_dir}/cxtvlive.m3u8" "${m3u_out_dir}/cxtvlive.m3u8" "${json_dir}/USA6.json"
match_epg_id_for_file "${m3u_in_dir}/cxtvlive.m3u8" "${m3u_out_dir}/cxtvlive.m3u8" "${json_dir}/USA7.json"
match_epg_id_for_file "${m3u_in_dir}/cxtvlive.m3u8" "${m3u_out_dir}/cxtvlive.m3u8" "${json_dir}/USA8.json"
match_epg_id_for_file "${m3u_in_dir}/cxtvlive.m3u8" "${m3u_out_dir}/cxtvlive.m3u8" "${json_dir}/USA9.json"
match_epg_id_for_file "${m3u_in_dir}/cxtvlive.m3u8" "${m3u_out_dir}/cxtvlive.m3u8" "${json_dir}/USA10.json"
match_epg_id_for_file "${m3u_in_dir}/cxtvlive.m3u8" "${m3u_out_dir}/cxtvlive.m3u8" "${json_dir}/USA11.json"
match_epg_id_for_file "${m3u_in_dir}/cxtvlive.m3u8" "${m3u_out_dir}/cxtvlive.m3u8" "${json_dir}/USA12.json"
match_epg_id_for_file "${m3u_in_dir}/cxtvlive.m3u8" "${m3u_out_dir}/cxtvlive.m3u8" "${json_dir}/USA13.json"
match_epg_id_for_file "${m3u_in_dir}/cxtvlive.m3u8" "${m3u_out_dir}/cxtvlive.m3u8" "${json_dir}/USA14.json"
match_epg_id_for_file "${m3u_in_dir}/cxtvlive.m3u8" "${m3u_out_dir}/cxtvlive.m3u8" "${json_dir}/USA15.json"
match_epg_id_for_file "${m3u_in_dir}/cxtvlive.m3u8" "${m3u_out_dir}/cxtvlive.m3u8" "${json_dir}/USA16.json"
match_epg_id_for_file "${m3u_in_dir}/cxtvlive.m3u8" "${m3u_out_dir}/cxtvlive.m3u8" "${json_dir}/USA17.json"

match_epg_id_for_file "${m3u_in_dir}/freetuxtv.m3u8" "${m3u_out_dir}/freetuxtv.m3u8" "${json_dir}/USA.json"
match_epg_id_for_file "${m3u_in_dir}/freetuxtv.m3u8" "${m3u_out_dir}/freetuxtv.m3u8" "${json_dir}/USA2.json"
match_epg_id_for_file "${m3u_in_dir}/freetuxtv.m3u8" "${m3u_out_dir}/freetuxtv.m3u8" "${json_dir}/USA3.json"
match_epg_id_for_file "${m3u_in_dir}/freetuxtv.m3u8" "${m3u_out_dir}/freetuxtv.m3u8" "${json_dir}/USA4.json"
match_epg_id_for_file "${m3u_in_dir}/freetuxtv.m3u8" "${m3u_out_dir}/freetuxtv.m3u8" "${json_dir}/USA5.json"
match_epg_id_for_file "${m3u_in_dir}/freetuxtv.m3u8" "${m3u_out_dir}/freetuxtv.m3u8" "${json_dir}/USA6.json"
match_epg_id_for_file "${m3u_in_dir}/freetuxtv.m3u8" "${m3u_out_dir}/freetuxtv.m3u8" "${json_dir}/USA7.json"
match_epg_id_for_file "${m3u_in_dir}/freetuxtv.m3u8" "${m3u_out_dir}/freetuxtv.m3u8" "${json_dir}/USA8.json"
match_epg_id_for_file "${m3u_in_dir}/freetuxtv.m3u8" "${m3u_out_dir}/freetuxtv.m3u8" "${json_dir}/USA9.json"
match_epg_id_for_file "${m3u_in_dir}/freetuxtv.m3u8" "${m3u_out_dir}/freetuxtv.m3u8" "${json_dir}/USA10.json"
match_epg_id_for_file "${m3u_in_dir}/freetuxtv.m3u8" "${m3u_out_dir}/freetuxtv.m3u8" "${json_dir}/USA11.json"
match_epg_id_for_file "${m3u_in_dir}/freetuxtv.m3u8" "${m3u_out_dir}/freetuxtv.m3u8" "${json_dir}/USA12.json"
match_epg_id_for_file "${m3u_in_dir}/freetuxtv.m3u8" "${m3u_out_dir}/freetuxtv.m3u8" "${json_dir}/USA13.json"
match_epg_id_for_file "${m3u_in_dir}/freetuxtv.m3u8" "${m3u_out_dir}/freetuxtv.m3u8" "${json_dir}/USA14.json"
match_epg_id_for_file "${m3u_in_dir}/freetuxtv.m3u8" "${m3u_out_dir}/freetuxtv.m3u8" "${json_dir}/USA15.json"
match_epg_id_for_file "${m3u_in_dir}/freetuxtv.m3u8" "${m3u_out_dir}/freetuxtv.m3u8" "${json_dir}/USA16.json"
match_epg_id_for_file "${m3u_in_dir}/freetuxtv.m3u8" "${m3u_out_dir}/freetuxtv.m3u8" "${json_dir}/USA17.json"

match_epg_id_for_file "${m3u_in_dir}/fslsports.m3u8" "${m3u_out_dir}/fslsports.m3u8" "${json_dir}/USA.json"
match_epg_id_for_file "${m3u_in_dir}/fslsports.m3u8" "${m3u_out_dir}/fslsports.m3u8" "${json_dir}/USA2.json"
match_epg_id_for_file "${m3u_in_dir}/fslsports.m3u8" "${m3u_out_dir}/fslsports.m3u8" "${json_dir}/USA3.json"
match_epg_id_for_file "${m3u_in_dir}/fslsports.m3u8" "${m3u_out_dir}/fslsports.m3u8" "${json_dir}/USA4.json"
match_epg_id_for_file "${m3u_in_dir}/fslsports.m3u8" "${m3u_out_dir}/fslsports.m3u8" "${json_dir}/USA5.json"
match_epg_id_for_file "${m3u_in_dir}/fslsports.m3u8" "${m3u_out_dir}/fslsports.m3u8" "${json_dir}/USA6.json"
match_epg_id_for_file "${m3u_in_dir}/fslsports.m3u8" "${m3u_out_dir}/fslsports.m3u8" "${json_dir}/USA7.json"
match_epg_id_for_file "${m3u_in_dir}/fslsports.m3u8" "${m3u_out_dir}/fslsports.m3u8" "${json_dir}/USA8.json"
match_epg_id_for_file "${m3u_in_dir}/fslsports.m3u8" "${m3u_out_dir}/fslsports.m3u8" "${json_dir}/USA9.json"
match_epg_id_for_file "${m3u_in_dir}/fslsports.m3u8" "${m3u_out_dir}/fslsports.m3u8" "${json_dir}/USA10.json"
match_epg_id_for_file "${m3u_in_dir}/fslsports.m3u8" "${m3u_out_dir}/fslsports.m3u8" "${json_dir}/USA11.json"
match_epg_id_for_file "${m3u_in_dir}/fslsports.m3u8" "${m3u_out_dir}/fslsports.m3u8" "${json_dir}/USA12.json"
match_epg_id_for_file "${m3u_in_dir}/fslsports.m3u8" "${m3u_out_dir}/fslsports.m3u8" "${json_dir}/USA13.json"
match_epg_id_for_file "${m3u_in_dir}/fslsports.m3u8" "${m3u_out_dir}/fslsports.m3u8" "${json_dir}/USA14.json"
match_epg_id_for_file "${m3u_in_dir}/fslsports.m3u8" "${m3u_out_dir}/fslsports.m3u8" "${json_dir}/USA15.json"
match_epg_id_for_file "${m3u_in_dir}/fslsports.m3u8" "${m3u_out_dir}/fslsports.m3u8" "${json_dir}/USA16.json"
match_epg_id_for_file "${m3u_in_dir}/fslsports.m3u8" "${m3u_out_dir}/fslsports.m3u8" "${json_dir}/USA17.json"

match_epg_id_for_file "${m3u_in_dir}/ustvgo.m3u8" "${m3u_out_dir}/ustvgo.m3u8" "${json_dir}/USA.json"
match_epg_id_for_file "${m3u_in_dir}/ustvgo.m3u8" "${m3u_out_dir}/ustvgo.m3u8" "${json_dir}/USA2.json"
match_epg_id_for_file "${m3u_in_dir}/ustvgo.m3u8" "${m3u_out_dir}/ustvgo.m3u8" "${json_dir}/USA3.json"
match_epg_id_for_file "${m3u_in_dir}/ustvgo.m3u8" "${m3u_out_dir}/ustvgo.m3u8" "${json_dir}/USA4.json"
match_epg_id_for_file "${m3u_in_dir}/ustvgo.m3u8" "${m3u_out_dir}/ustvgo.m3u8" "${json_dir}/USA5.json"
match_epg_id_for_file "${m3u_in_dir}/ustvgo.m3u8" "${m3u_out_dir}/ustvgo.m3u8" "${json_dir}/USA6.json"
match_epg_id_for_file "${m3u_in_dir}/ustvgo.m3u8" "${m3u_out_dir}/ustvgo.m3u8" "${json_dir}/USA7.json"
match_epg_id_for_file "${m3u_in_dir}/ustvgo.m3u8" "${m3u_out_dir}/ustvgo.m3u8" "${json_dir}/USA8.json"
match_epg_id_for_file "${m3u_in_dir}/ustvgo.m3u8" "${m3u_out_dir}/ustvgo.m3u8" "${json_dir}/USA9.json"
match_epg_id_for_file "${m3u_in_dir}/ustvgo.m3u8" "${m3u_out_dir}/ustvgo.m3u8" "${json_dir}/USA10.json"
match_epg_id_for_file "${m3u_in_dir}/ustvgo.m3u8" "${m3u_out_dir}/ustvgo.m3u8" "${json_dir}/USA11.json"
match_epg_id_for_file "${m3u_in_dir}/ustvgo.m3u8" "${m3u_out_dir}/ustvgo.m3u8" "${json_dir}/USA12.json"
match_epg_id_for_file "${m3u_in_dir}/ustvgo.m3u8" "${m3u_out_dir}/ustvgo.m3u8" "${json_dir}/USA13.json"
match_epg_id_for_file "${m3u_in_dir}/ustvgo.m3u8" "${m3u_out_dir}/ustvgo.m3u8" "${json_dir}/USA14.json"
match_epg_id_for_file "${m3u_in_dir}/ustvgo.m3u8" "${m3u_out_dir}/ustvgo.m3u8" "${json_dir}/USA15.json"
match_epg_id_for_file "${m3u_in_dir}/ustvgo.m3u8" "${m3u_out_dir}/ustvgo.m3u8" "${json_dir}/USA16.json"
match_epg_id_for_file "${m3u_in_dir}/ustvgo.m3u8" "${m3u_out_dir}/ustvgo.m3u8" "${json_dir}/USA17.json"

match_epg_id_for_file "${m3u_in_dir}/moreiptv.m3u8" "${m3u_out_dir}/moreiptv.m3u8" "${json_dir}/USA.json"
match_epg_id_for_file "${m3u_in_dir}/moreiptv.m3u8" "${m3u_out_dir}/moreiptv.m3u8" "${json_dir}/USA2.json"
match_epg_id_for_file "${m3u_in_dir}/moreiptv.m3u8" "${m3u_out_dir}/moreiptv.m3u8" "${json_dir}/USA3.json"
match_epg_id_for_file "${m3u_in_dir}/moreiptv.m3u8" "${m3u_out_dir}/moreiptv.m3u8" "${json_dir}/USA4.json"
match_epg_id_for_file "${m3u_in_dir}/moreiptv.m3u8" "${m3u_out_dir}/moreiptv.m3u8" "${json_dir}/USA5.json"
match_epg_id_for_file "${m3u_in_dir}/moreiptv.m3u8" "${m3u_out_dir}/moreiptv.m3u8" "${json_dir}/USA6.json"
match_epg_id_for_file "${m3u_in_dir}/moreiptv.m3u8" "${m3u_out_dir}/moreiptv.m3u8" "${json_dir}/USA7.json"
match_epg_id_for_file "${m3u_in_dir}/moreiptv.m3u8" "${m3u_out_dir}/moreiptv.m3u8" "${json_dir}/USA8.json"
match_epg_id_for_file "${m3u_in_dir}/moreiptv.m3u8" "${m3u_out_dir}/moreiptv.m3u8" "${json_dir}/USA9.json"
match_epg_id_for_file "${m3u_in_dir}/moreiptv.m3u8" "${m3u_out_dir}/moreiptv.m3u8" "${json_dir}/USA10.json"
match_epg_id_for_file "${m3u_in_dir}/moreiptv.m3u8" "${m3u_out_dir}/moreiptv.m3u8" "${json_dir}/USA11.json"
match_epg_id_for_file "${m3u_in_dir}/moreiptv.m3u8" "${m3u_out_dir}/moreiptv.m3u8" "${json_dir}/USA12.json"
match_epg_id_for_file "${m3u_in_dir}/moreiptv.m3u8" "${m3u_out_dir}/moreiptv.m3u8" "${json_dir}/USA13.json"
match_epg_id_for_file "${m3u_in_dir}/moreiptv.m3u8" "${m3u_out_dir}/moreiptv.m3u8" "${json_dir}/USA14.json"
match_epg_id_for_file "${m3u_in_dir}/moreiptv.m3u8" "${m3u_out_dir}/moreiptv.m3u8" "${json_dir}/USA15.json"
match_epg_id_for_file "${m3u_in_dir}/moreiptv.m3u8" "${m3u_out_dir}/moreiptv.m3u8" "${json_dir}/USA16.json"
match_epg_id_for_file "${m3u_in_dir}/moreiptv.m3u8" "${m3u_out_dir}/moreiptv.m3u8" "${json_dir}/USA17.json"

match_epg_id_for_file "${m3u_in_dir}/pbsall.m3u8" "${m3u_out_dir}/pbsall.m3u8" "${json_dir}/USA.json"
match_epg_id_for_file "${m3u_in_dir}/pbsall.m3u8" "${m3u_out_dir}/pbsall.m3u8" "${json_dir}/USA2.json"
match_epg_id_for_file "${m3u_in_dir}/pbsall.m3u8" "${m3u_out_dir}/pbsall.m3u8" "${json_dir}/USA3.json"
match_epg_id_for_file "${m3u_in_dir}/pbsall.m3u8" "${m3u_out_dir}/pbsall.m3u8" "${json_dir}/USA4.json"
match_epg_id_for_file "${m3u_in_dir}/pbsall.m3u8" "${m3u_out_dir}/pbsall.m3u8" "${json_dir}/USA5.json"
match_epg_id_for_file "${m3u_in_dir}/pbsall.m3u8" "${m3u_out_dir}/pbsall.m3u8" "${json_dir}/USA6.json"
match_epg_id_for_file "${m3u_in_dir}/pbsall.m3u8" "${m3u_out_dir}/pbsall.m3u8" "${json_dir}/USA7.json"
match_epg_id_for_file "${m3u_in_dir}/pbsall.m3u8" "${m3u_out_dir}/pbsall.m3u8" "${json_dir}/USA8.json"
match_epg_id_for_file "${m3u_in_dir}/pbsall.m3u8" "${m3u_out_dir}/pbsall.m3u8" "${json_dir}/USA9.json"
match_epg_id_for_file "${m3u_in_dir}/pbsall.m3u8" "${m3u_out_dir}/pbsall.m3u8" "${json_dir}/USA10.json"
match_epg_id_for_file "${m3u_in_dir}/pbsall.m3u8" "${m3u_out_dir}/pbsall.m3u8" "${json_dir}/USA11.json"
match_epg_id_for_file "${m3u_in_dir}/pbsall.m3u8" "${m3u_out_dir}/pbsall.m3u8" "${json_dir}/USA12.json"
match_epg_id_for_file "${m3u_in_dir}/pbsall.m3u8" "${m3u_out_dir}/pbsall.m3u8" "${json_dir}/USA13.json"
match_epg_id_for_file "${m3u_in_dir}/pbsall.m3u8" "${m3u_out_dir}/pbsall.m3u8" "${json_dir}/USA14.json"
match_epg_id_for_file "${m3u_in_dir}/pbsall.m3u8" "${m3u_out_dir}/pbsall.m3u8" "${json_dir}/USA15.json"
match_epg_id_for_file "${m3u_in_dir}/pbsall.m3u8" "${m3u_out_dir}/pbsall.m3u8" "${json_dir}/USA16.json"
match_epg_id_for_file "${m3u_in_dir}/pbsall.m3u8" "${m3u_out_dir}/pbsall.m3u8" "${json_dir}/USA17.json"

match_epg_id_for_file "${m3u_in_dir}/plutoall.m3u8" "${m3u_out_dir}/plutoall.m3u8" "${json_dir}/USA.json"
match_epg_id_for_file "${m3u_in_dir}/plutoall.m3u8" "${m3u_out_dir}/plutoall.m3u8" "${json_dir}/USA2.json"
match_epg_id_for_file "${m3u_in_dir}/plutoall.m3u8" "${m3u_out_dir}/plutoall.m3u8" "${json_dir}/USA3.json"
match_epg_id_for_file "${m3u_in_dir}/plutoall.m3u8" "${m3u_out_dir}/plutoall.m3u8" "${json_dir}/USA4.json"
match_epg_id_for_file "${m3u_in_dir}/plutoall.m3u8" "${m3u_out_dir}/plutoall.m3u8" "${json_dir}/USA5.json"
match_epg_id_for_file "${m3u_in_dir}/plutoall.m3u8" "${m3u_out_dir}/plutoall.m3u8" "${json_dir}/USA6.json"
match_epg_id_for_file "${m3u_in_dir}/plutoall.m3u8" "${m3u_out_dir}/plutoall.m3u8" "${json_dir}/USA7.json"
match_epg_id_for_file "${m3u_in_dir}/plutoall.m3u8" "${m3u_out_dir}/plutoall.m3u8" "${json_dir}/USA8.json"
match_epg_id_for_file "${m3u_in_dir}/plutoall.m3u8" "${m3u_out_dir}/plutoall.m3u8" "${json_dir}/USA9.json"
match_epg_id_for_file "${m3u_in_dir}/plutoall.m3u8" "${m3u_out_dir}/plutoall.m3u8" "${json_dir}/USA10.json"
match_epg_id_for_file "${m3u_in_dir}/plutoall.m3u8" "${m3u_out_dir}/plutoall.m3u8" "${json_dir}/USA11.json"
match_epg_id_for_file "${m3u_in_dir}/plutoall.m3u8" "${m3u_out_dir}/plutoall.m3u8" "${json_dir}/USA12.json"
match_epg_id_for_file "${m3u_in_dir}/plutoall.m3u8" "${m3u_out_dir}/plutoall.m3u8" "${json_dir}/USA13.json"
match_epg_id_for_file "${m3u_in_dir}/plutoall.m3u8" "${m3u_out_dir}/plutoall.m3u8" "${json_dir}/USA14.json"
match_epg_id_for_file "${m3u_in_dir}/plutoall.m3u8" "${m3u_out_dir}/plutoall.m3u8" "${json_dir}/USA15.json"
match_epg_id_for_file "${m3u_in_dir}/plutoall.m3u8" "${m3u_out_dir}/plutoall.m3u8" "${json_dir}/USA16.json"
match_epg_id_for_file "${m3u_in_dir}/plutoall.m3u8" "${m3u_out_dir}/plutoall.m3u8" "${json_dir}/USA17.json"



