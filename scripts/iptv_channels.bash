#!/bin/bash

#TIMEOUT
TIMEOUT=10.0

for file in ./m3u8/*.m3u
do
		NAME=$(basename "$file" .m3u)
		if [ -f "./"$NAME"_checked.m3u" ]
			then
				echo ""$NAME"_checked.m3u"" already exists..."
			else
				echo "--------------------------------------------------------------------------------"
				echo "$NAME"
				python3 ./scripts/streamcleaner.py --timeout $TIMEOUT --input-file "$file" --output-file ""$NAME"_checked.m3u"
				echo "--------------------------------------------------------------------------------"
				mv ""$NAME"_checked.m3u" .
		fi
done

for file in ./*_checked.m3u
do
		NAME=$(basename "$file" .m3u)
		cat ./"$file" >> ./M3U_COMPLETE.m3u
done
