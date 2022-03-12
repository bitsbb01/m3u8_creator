# python3
# m3usplitter.py, by lakeconstance78@wolke7.net
#
# this script:
# 				1. Splits M3U file in files by group
#
# requirements: Python3
#
# command line: m3usplitter.py M3UFILE..m3u
#
# TODO:

import re
import argparse
from io import open
import os
import string

# PATTERN FOR CHANNEL-INFORMATION
PATTERN = re.compile('#EXTINF:.*group-title="(.*?)".*,(.*)\nhttps?:\/\/(.*)\n')
# group(1) GROUP-TITLE
# group(2) CHANNEL-NAME
# group(3) CHANNEL-LINK

CHECK = 0
GROUPNAME = None
EXTINF = None
LINK = None
MERGECHANNELS = None

CHANNELCOUNT = 0
CHCOUNT = 0
MERGECOUNT = 0
MECOUNT = 0
SORTCOUNT = 0
SOCOUNT = 0

# READ INPUT FILE
parser = argparse.ArgumentParser()
parser.add_argument('M3UINPUT')
args = parser.parse_args()
INPUTFILE = open(args.M3UINPUT)
CHANNELS = INPUTFILE.read()

#SPLIT M3U FILE IN FILES BY GROUP
print("----------------------------------------------")
print("Spliting " + args.M3UINPUT)
print("----------------------------------------------")
for match in PATTERN.finditer(CHANNELS):

    CHANNEL = re.search(PATTERN, match.group(0))
    GROUPNAME = match.group(1).title()
    CHANNEL = re.sub(match.group(1), GROUPNAME.title(), match.group(0), flags=re.I|re.M)

    # GENERATE FILENAME FROM GROUPNAME
    if GROUPNAME:
        FILENAME = GROUPNAME + ".m3u"
        FILENAME = string.capwords(FILENAME)
    else: FILENAME = "m3u_emptygroup.m3u"

    # CHECK LINE 1 IF #EXTM3U EXISTS
    if os.path.exists(FILENAME):
        with open(FILENAME,'r', encoding='utf-8') as OUTPUTFILE:
            CONTENT = OUTPUTFILE.read()
            FIRST = CONTENT.split('\n', 1)[0]
            if '#EXTM3U' != FIRST:
                print(FILENAME + " -> #EXTM3U does not exists -> insert in line 1")
                with open(FILENAME+'.tempfile','w', encoding='utf-8') as t:
                    t.write('#EXTM3U\n' + CONTENT)
                os.rename(FILENAME+'.tempfile', FILENAME)

    # WRITING CHANNEL TO FILE
    with open(FILENAME,'a', encoding='utf-8') as OUTPUTFILE:
        CHANNEL = match.group(0)
        OUTPUTFILE.write(CHANNEL)
        OUTPUTFILE.write('\n')