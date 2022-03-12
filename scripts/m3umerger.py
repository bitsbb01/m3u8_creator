# python3
# m3umerger.py, by lakeconstance78@wolke7.net
#
# this script:
# 				1. Merges all m3u files in the directory to m3u_merge.m3u
#
# requirements: Python3 inlcuding re, io, os
#
# command line: m3umerger.py
#
# TODO:

import re
from io import open
import os

DIRECTORY = r'.'

# PATTERN FOR CHANNEL-INFORMATION
PATTERN = re.compile('#EXTINF:.*group-title="(.*?)".*,(.*)\nhttps?:\/\/(.*)\n')
# group(1) GROUP-TITLE
# group(2) CHANNEL-NAME
# group(3) CHANNEL-LINK

for FILENAME in os.listdir(DIRECTORY):
    if (FILENAME.endswith(".M3U") | FILENAME.endswith(".m3u")) and FILENAME != 'm3u_merge.m3u':
        with open(FILENAME, 'r') as INPUTFILE:
            CHANNELS = INPUTFILE.read()
            for match in PATTERN.finditer(CHANNELS):
                with open('m3u_merge.m3u','a', encoding='utf-8') as MERGEFILE:
                    CHANNEL = match.group(0)
                    MERGECHANNELS = MERGEFILE.write(CHANNEL)
    continue

# CHECK LINE 1 IF #EXTM3U EXISTS
if os.path.exists('m3u_merge.m3u'):
    with open('m3u_merge.m3u','r', encoding='utf-8') as OUTPUTFILE:
        CONTENT = OUTPUTFILE.read()
        FIRST = CONTENT.split('\n', 1)[0]
        if '#EXTM3U' != FIRST:
            print('m3u_merge.m3u' + " -> #EXTM3U does not exists -> insert in line 1")
            with open('m3u_merge.m3u'+'.tempfile','w', encoding='utf-8') as t:
                t.write('#EXTM3U\n' + CONTENT)
            os.rename('m3u_merge.m3u'+'.tempfile', 'm3u_merge.m3u')