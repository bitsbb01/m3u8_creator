#!/bin/bash
# iptv_channels.bash, by lakeconstance78@wolke7.net
#
# this script: 
# 				1.  Download my IPTV-channel collection from my playlist repository
#					https://github.com/lakeconstance78/IPTV-channels
#				2.	Download m3u channel lists defined below
#				3.	Checks every links in all m3u channel lists and safe them
#					under *_checked.
#					The checking tool is used from
#					https://github.com/FutureSharks/iptv-stream-cleaner	
# 					
# requirements: bash
#
# command line: bash iptv_channels.bash
#				
# todo
# - 

#PUT YOUR M3U PLAYLISTS HERE
#https://github.com/iptv-org/iptv
M3U_PLAYLIST_1=https://iptv-org.github.io/iptv/index.country.m3u
#https://github.com/Free-IPTV/Countries
M3U_PLAYLIST_2=https://raw.githubusercontent.com/Free-IPTV/Countries/master/ZZ_PLAYLIST_ALL_TV.m3u
#https://github.com/Free-TV/IPTV
M3U_PLAYLIST_3=https://raw.githubusercontent.com/Free-TV/IPTV/master/playlist.m3u8
#https://github.com/jnk22/kodinerds-iptv
M3U_PLAYLIST_4=http://bit.ly/kn-clean
#https://github.com/hayatiptv/iptv
M3U_PLAYLIST_5=https://tinyurl.com/skaae8k

#TIMEOUT
TIMEOUT=10.0

rm iptv-channels -r

echo "--------------------------------------------------------------------------------"
git clone https://github.com/lakeconstance78/iptv-channels.git

#DOWNLOAD PLAYLISTS
wget $M3U_PLAYLIST_1 -O ./iptv-channels/M3U_PLAYLIST_1.m3u
wget $M3U_PLAYLIST_2 -O ./iptv-channels/M3U_PLAYLIST_2.m3u
wget $M3U_PLAYLIST_3 -O ./iptv-channels/M3U_PLAYLIST_3.m3u
wget $M3U_PLAYLIST_4 -O ./iptv-channels/M3U_PLAYLIST_4.m3u
wget $M3U_PLAYLIST_5 -O ./iptv-channels/M3U_PLAYLIST_5.m3u

echo "--------------------------------------------------------------------------------"
for file in ./iptv-channels/*.m3u
do
		NAME=$(basename "$file" .m3u)
		if [ -f "./"$NAME"_checked.m3u" ]
			then
				echo ""$NAME"_checked.m3u"" already exists..."
			else
				echo "--------------------------------------------------------------------------------"
				echo "$NAME"
				python3 ./iptv-channels/stream-cleaner.py --timeout $TIMEOUT --input-file "$file" --output-file ""$NAME"_checked.m3u"
				echo "--------------------------------------------------------------------------------"
				mv ""$NAME"_checked.m3u" .
		fi
done

for file in ./*_checked.m3u
do
		NAME=$(basename "$file" .m3u)
		cat ./"$file" >> ./M3U_COMPLETE.m3u
done