"""Script to convert m3u4u channel files to a fake m3u playlist."""

import argparse
import json
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from ez_m3u8_creator import m3u8


def main():
    """Run the main function."""
    parser = argparse.ArgumentParser()
    parser.add_argument('-jd', '--json_dir', help='The directory containing the json files.', required=True)
    parser.add_argument('-of', '--out_file', help='The path to the file to store', required=True)
    args = parser.parse_args()

    if (not os.path.exists(args.json_dir)) or not os.path.isdir(args.json_dir):
        raise ValueError(F'"{args.json_dir}" is not a vaid directory')

    m3u8_file = m3u8.M3U8File()

    for filename in os.listdir(args.json_dir):
        if not filename.lower().endswith('.json'):
            continue

        file_path = os.path.join(args.json_dir, filename)
        with open(file_path, 'r', encoding='utf-8') as file_ptr:
            data = json.load(file_ptr)
            for channel in data:
                m3u8_file.add_channel(name=channel['name'], url=F'''http://{channel['tvgid']}''', channel_id=channel['tvgid'])

    m3u8_file.write_file(args.out_file)


if __name__ == '__main__':
    main()
