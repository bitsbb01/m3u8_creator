"""Handle data import and convertion for the iptvcat_scraper files."""

import json
import os

from ez_m3u8_creator import m3u8


INCLUDE_STATUS_LIST = ['online', 'offline']
TAG_STATUS_LIST = ['offline']
LIVELINESS_MIN = 70


class IptvCatFile():
    """A single IptvCat scraper file."""

    def __init__(self, file_path):
        """Create a iptv cat file object."""
        self.path = file_path
        self.data = []

        self._parse_file()

    def filter_channels(self, *, status_list, liveliness_min):
        """Filter the channels by the given attributes."""
        new_data = []
        for entry in self.data:
            if entry['status'] not in status_list:
                continue

            if int(entry['liveliness']) < liveliness_min:
                continue

            new_data.append(entry)

        self.data = new_data

    def write_playlist(self, *, out_path, tag_status_list=None):
        """Write the playlist to the given file."""
        m3u8_file = m3u8.M3U8File()

        for channel in self:
            name = F'''{channel['channel']} [{channel['liveliness']}]'''
            if tag_status_list and channel['status'] in tag_status_list:
                name += F'''[{channel['status']}]'''

            m3u8_file.add_channel(name=name, url=channel['link'])

        m3u8_file.write_file(out_path)

    def _parse_file(self):
        """Parse the file."""
        with open(self.path, 'r', encoding='utf-8') as file_ptr:
            self.data = json.load(file_ptr)

    def __len__(self):
        return len(self.data)

    def __iter__(self):
        return iter(self.data)


def convert_json_dir_to_m3u8(*, in_dir, out_dir):
    """Convert the json files to the m3u8 files."""
    for root, _, files in os.walk(in_dir):
        for filename in files:
            if not filename.lower().endswith('.json'):
                continue

            base_name = os.path.splitext(filename)[0]
            from_file_path = os.path.join(root, filename)
            out_file_path = os.path.join(out_dir, base_name + '.m3u8')

            iptvcat_file = IptvCatFile(from_file_path)
            iptvcat_file.filter_channels(status_list=INCLUDE_STATUS_LIST, liveliness_min=LIVELINESS_MIN)
            iptvcat_file.write_playlist(out_path=out_file_path, tag_status_list=TAG_STATUS_LIST)
