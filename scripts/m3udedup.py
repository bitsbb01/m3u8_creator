# python3
# m3udedup.py, by lakeconstance78@wolke7.net
#
# this script:
# 				1. Sortout duplicate files
#               2. Renames the files, as defined in m3urenames.txt
#
# requirements: Python3
#
# command line: m3udedup.py M3UFILE..m3u
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

SORTOUTROUNDS=1 # DEFINES HOW MANY LOOPS THE DEDUPLICATE MECHANISM WILL DO
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

print("Searching for duplicates in " + args.M3UINPUT)
print("----------------------------------------------")

# SEARCHING FOR DUPLICATES IN INPUTFILE
for i in range (SORTOUTROUNDS+1):
    for match in PATTERN.finditer(CHANNELS):
        CHANNELCOUNT = CHANNELCOUNT + 1
        CHCOUNT = CHANNELCOUNT / (i+1)
        if os.path.exists('m3u_merge_'+str(i)+'.m3u'):
            with open('m3u_merge_'+str(i)+'.m3u','r', encoding='utf-8') as MERGEFILE:
                MERGECHANNELS = MERGEFILE.read()
        else:
            with open('m3u_merge_'+str(i)+'.m3u','w', encoding='utf-8') as MERGEFILE:
                MERGEFILE.write('#EXTM3U\n')

        CHANNEL = match.group(0)

        # OPEN FILE WITH RENAME INFOS AND RENAME ALL GROUPS THAT MATCH TEXT IN RENAME INFOS
        with open('m3urenames.txt', 'r') as RENAMEFILE:
                for line in RENAMEFILE:
                    TEXT, RENAME = line.split(",")
                    RENAME = RENAME.rstrip()
                    if re.findall(TEXT, match.group(1), flags=re.I|re.M):
                        GROUPNAMEBF = match.group(1)
                        CHANNEL = re.sub(match.group(1), RENAME, match.group(0), flags=re.I)
                        GROUPNAME = re.search(PATTERN, CHANNEL).group(1)
                        if (GROUPNAME != None) and (GROUPNAME != GROUPNAMEBF):
                            print("Groupname of Channel " + re.search(PATTERN, CHANNEL).group(2) + " renamed from " + GROUPNAMEBF + " to " + GROUPNAME)
                    continue

        """ NOT WORKING YET
        # LOOKING FOR SPECIAL INTEREST e.g. MUSIC OR BROADCAST COMPANIES
        if re.findall('.*Mus?z?ic?k?.*', CHANNEL, flags=re.I) or re.findall('.*MTV.*', CHANNEL, flags=re.I) or re.findall('.*Stingray.*', CHANNEL, flags=re.I):
            if re.search(PATTERN, CHANNEL) != None:
                GROUPNAMEBF = match.group(1)
                CHANNEL = re.sub(match.group(1), 'Music', match.group(0), flags=re.I)
                if re.search(PATTERN, CHANNEL) != None:
                    GROUPNAME = re.search(PATTERN, CHANNEL).group(1)
                    if (GROUPNAME != None) and (GROUPNAME != GROUPNAMEBF):
                        print("Groupname of Channel " + re.search(PATTERN, CHANNEL).group(2) + " renamed from " + GROUPNAMEBF + " to " + GROUPNAME)
        if re.findall('.*Pluto.*', CHANNEL, flags=re.I|re.M):
            if re.search(PATTERN, CHANNEL) != None:
                GROUPNAMEBF = match.group(1)
                CHANNEL = re.sub(match.group(1), 'Pluto', match.group(0), flags=re.I)
                if re.search(PATTERN, CHANNEL) != None:
                    GROUPNAME = re.search(PATTERN, CHANNEL).group(1)
                    if (GROUPNAME != None) and (GROUPNAME != GROUPNAMEBF):
                        print("Groupname of Channel " + re.search(PATTERN, CHANNEL).group(2) + " renamed from " + GROUPNAMEBF + " to " + GROUPNAME)
        """

        #CHANNEL = match.group(0)

        # RENAMES FOR CHANNEL TAGS
        # DELETE HD, FHD, UHD TAGS
        CHANNEL = re.sub('F?U?HD','',CHANNEL)
        CHANNEL = re.sub('SD','',CHANNEL)
        # DELETE TEXT BETWEEN () AND [] e.g. (360p) OR [geo-blocked]
        CHANNEL = re.sub('\(.*?\)','',CHANNEL)
        CHANNEL = re.sub('\[.*?\]','',CHANNEL)

        if MERGECHANNELS != None:
            # COMPARE IF CHANNEL NAME AND LINK ALREAD EXISTS
            if re.search(PATTERN, CHANNEL).group(2) and re.search(PATTERN, CHANNEL).group(3) in MERGECHANNELS:
                print("Channel " + re.search(PATTERN, CHANNEL).group(2) + " -> already exists...")
                SORTCOUNT = SORTCOUNT + 1
                SOCOUNT = SORTCOUNT / (i+1)
            # IF NO WRITE ACTUAL MATCH IN MERGEFILE.
            # FIRST ROUND USES ORIGINAL CHANNEL NAMES.
            # SECOND ROUND USES CHANNEL NAMES WITHOUT HD, FHD, 360p..., GEO-BLOCKED TAGS
            else:
                with open('m3u_merge_'+str(i)+'.m3u','a', encoding='utf-8') as MERGEFILE:
                    MERGECOUNT = MERGECOUNT + 1
                    MECOUNT = MERGECOUNT / (i+1)
                    MERGEFILE.write(CHANNEL)
    # USE LAST ROUND AS INPUT
    INPUTFILE = open('m3u_merge_'+str(i)+'.m3u')
    CHANNELS = INPUTFILE.read()

print("----------------------------------------------")
print("finished: ", args.M3UINPUT, " -> channels: ", int(CHCOUNT), " -> merged: ", int(MECOUNT), " -> sorted out: ", int(SOCOUNT))