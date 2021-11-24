"""Script to convert iptvcat json files to m3u8."""

import argparse
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from ez_m3u8_creator import m3u8


def main():
    """Run the main function."""
    parser = argparse.ArgumentParser()
    parser.add_argument('-mi', '--merge_into_file', help='The file to merge into', required=True)
    parser.add_argument('-mf', '--merge_from_file', help='The file to merge from.', required=True)
    args = parser.parse_args()

    print('merge_into_file', args.merge_into_file)
    print('merge_from_file', args.merge_from_file)

    if (not os.path.exists(args.merge_into_file)) or not os.path.isfile(args.merge_into_file):
        raise ValueError(F'"{args.merge_into_file}" is not a vaid file')
    if (not os.path.exists(args.merge_from_file)) or not os.path.isfile(args.merge_from_file):
        raise ValueError(F'"{args.merge_from_file}" is not a vaid file')

    m3u8.merge_m3u8_files(merge_into_path=args.merge_into_file, merge_from_path=args.merge_from_file)


if __name__ == '__main__':
    main()
