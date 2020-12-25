"""Script to convert iptvcat json files to m3u8."""

import argparse
import json
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from ez_m3u8_creator import m3u8


def main():
    """Run the main function."""
    parser = argparse.ArgumentParser()
    parser.add_argument('-cf', '--category_file', help='The file containing category information.', required=True)
    parser.add_argument('-mi', '--m3u8_in_dir', help='The directory to read the m3u8 files.', required=True)
    parser.add_argument('-mo', '--m3u8_out_dir', help='The directory to store the m3u8 files.', required=True)
    args = parser.parse_args()

    print('category_file', args.category_file)
    print('m3u8_in_dir', args.m3u8_in_dir)
    print('m3u8_out_dir', args.m3u8_out_dir)

    if (not os.path.exists(args.category_file)) or not os.path.isfile(args.category_file):
        raise ValueError(F'"{args.category_file}" is not a vaid file')
    if (not os.path.exists(args.m3u8_in_dir)) or not os.path.isdir(args.m3u8_in_dir):
        raise ValueError(F'"{args.m3u8_in_dir}" is not a vaid directory')
    if (not os.path.exists(args.m3u8_out_dir)) or not os.path.isdir(args.m3u8_out_dir):
        raise ValueError(F'"{args.m3u8_out_dir}" is not a vaid directory')

    category_data = []
    with open(args.category_file, 'r', encoding='utf-8') as file_ptr:
        category_data = json.load(file_ptr)

    for filename in os.listdir(args.m3u8_in_dir):
        if not filename.lower().endswith('.m3u8') and not filename.lower().endswith('.m3u'):
            continue

        print('category_data', category_data)

        m3u8_file = m3u8.M3U8File(os.path.join(args.m3u8_in_dir, filename))
        m3u8_file.add_groups_from_category_dic(category_data)

        out_path = os.path.join(os.path.join(args.m3u8_out_dir, filename))
        m3u8_file.write_file(out_path)


if __name__ == '__main__':
    main()
