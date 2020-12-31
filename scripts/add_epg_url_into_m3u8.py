"""Script to add an EPG url to m3u8 files."""

import argparse
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from ez_m3u8_creator import m3u8


def main():
    """Run the main function."""
    parser = argparse.ArgumentParser()
    parser.add_argument('-eu', '--epg_url', help='The epg url.', required=True)
    parser.add_argument('-mi', '--m3u8_in_dir', help='The directory to read the m3u8 files.', required=True)
    parser.add_argument('-mo', '--m3u8_out_dir', help='The directory to store the m3u8 files.', required=True)
    args = parser.parse_args()

    print('epg_url', args.epg_url)
    print('m3u8_in_dir', args.m3u8_in_dir)
    print('m3u8_out_dir', args.m3u8_out_dir)

    if (not os.path.exists(args.m3u8_in_dir)) or not os.path.isdir(args.m3u8_in_dir):
        raise ValueError(F'"{args.m3u8_in_dir}" is not a vaid directory')
    if (not os.path.exists(args.m3u8_out_dir)) or not os.path.isdir(args.m3u8_out_dir):
        raise ValueError(F'"{args.m3u8_out_dir}" is not a vaid directory')

    for filename in os.listdir(args.m3u8_in_dir):
        if not filename.lower().endswith('.m3u8') and not filename.lower().endswith('.m3u'):
            continue

        m3u8_file = m3u8.M3U8File(os.path.join(args.m3u8_in_dir, filename))

        m3u8_file.epg_tvg_url = args.epg_url
        m3u8_file.epg_url_tvg = args.epg_url
        m3u8_file.epg_x_tvg_url = args.epg_url

        out_path = os.path.join(os.path.join(args.m3u8_out_dir, filename))
        m3u8_file.write_file(out_path)


if __name__ == '__main__':
    main()
