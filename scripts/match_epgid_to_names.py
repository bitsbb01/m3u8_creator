"""Script to convert m3u4u channel files to a fake m3u playlist."""

import argparse
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from ez_m3u8_creator import m3u8


def main():
    """Run the main function."""
    parser = argparse.ArgumentParser()
    parser.add_argument('-if', '--input_file', help='The m3u playlist to process.', required=True)
    parser.add_argument('-of', '--out_file', help='The m3u playlist to write to', required=True)
    parser.add_argument('-jf', '--json_file', help='The json file with the channel info.', required=True)
    args = parser.parse_args()

    if (not os.path.exists(args.input_file)) or not os.path.isfile(args.input_file):
        # raise ValueError(F'"{args.input_file}" is not a vaid file')
        print(F'"{args.input_file}" is not a vaid file')
    elif (not os.path.exists(args.json_file)) or not os.path.isfile(args.json_file):
        # raise ValueError(F'"{args.json_file}" is not a vaid file')
        print(F'"{args.json_file}" is not a vaid file')
    else:
        m3u8_file = m3u8.M3U8File(args.input_file)

        count = m3u8.match_epg_channels(m3u8_file, args.json_file)
        print('FOUND:', count)

        m3u8_file.write_file(args.out_file)


if __name__ == '__main__':
    main()
