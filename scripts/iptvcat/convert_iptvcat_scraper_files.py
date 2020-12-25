"""Script to convert iptvcat json files to m3u8."""

import argparse
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from ez_m3u8_creator.iptvcat import iptvcat_scraper_converter
from ez_m3u8_creator import project_logger


def main():
    """Run the main function."""
    parser = argparse.ArgumentParser()
    parser.add_argument('json_dir', help='The directory containing the Json files.')
    parser.add_argument('m3u8_dir', help='The directory to store the m3u8 files.')
    args = parser.parse_args()

    if (not os.path.exists(args.json_dir)) or (not os.path.isdir(args.json_dir)):
        raise ValueError(F'"{args.json_dir}" is not a vaid directory')
    if (not os.path.exists(args.m3u8_dir)) or (not os.path.isdir(args.m3u8_dir)):
        raise ValueError(F'"{args.m3u8_dir}" is not a vaid directory')

    iptvcat_scraper_converter.convert_json_dir_to_m3u8(
        in_dir=args.json_dir, out_dir=args.m3u8_dir
    )


if __name__ == '__main__':
    main()
