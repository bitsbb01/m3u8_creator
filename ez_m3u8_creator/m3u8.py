"""Code to handle m3u8 file type."""

import json
import re

M3U8_OPENING_TAG = '#EXTM3U'
M3U8_CHANNEL_INFO_PREFIX = '#EXTINF:'
M3U8_SPECIAL_LINE_START_TAG = '#'


class M3U8File():
    """An m3u8 file representation."""

    def __init__(self, file_path=None):
        """Initialize the M3U8 file."""
        self.channel_url_dict = {}
        self.epg_tvg_url = ""
        self.epg_url_tvg = ""
        self.epg_x_tvg_url = ""

        if file_path is not None:
            self._load_file(file_path)

    def add_channel(self, *, name, url, group='', channel_id=''):
        """Add a channel to the file."""
        if url not in self.channel_url_dict:
            self.channel_url_dict[url] = []
        self.channel_url_dict[url].append({
            'name': name,
            'url': url,
            'group': group,
            'id': channel_id,
        })

    def add_groups_from_category_dic(self, category_dic, *, overwrite=True):
        """Calculate the groups based on the given json file."""
        for _, channel_list in self.channel_url_dict.items():
            for channel in channel_list:
                categories = get_categories_from_json(channel_name=channel['name'], json_data=category_dic)
                if categories and overwrite:
                    channel['group'] = ';'.join(categories)

    def merge(self, other_m3u8_file):
        """Merge the other_m3u8_file into this one."""
        for _, channel_list in other_m3u8_file.channel_url_dict.items():
            for channel in channel_list:
                self.add_channel(
                    name=channel['name'], url=channel['url'],
                    group=channel['group'], channel_id=channel['id'])

    def remove_duplicate_urls(self):
        """Remove duplicate URLs from the list."""
        for url, _ in self.channel_url_dict.items():
            if len(self.channel_url_dict[url]) > 1:
                self.channel_url_dict[url] = self.channel_url_dict[url][:1]

    def _load_file(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file_ptr:
            details = {}
            for line in file_ptr:
                line = line.rstrip()
                if line.startswith(M3U8_OPENING_TAG):
                    # Get the EPG Url
                    result = re.search('tvg-url="(?P<epg_tvg_url>.*?)"', line)
                    self.epg_tvg_url = result.group('epg_tvg_url') if bool(result) else ''
                    result = re.search('url-tvg="(?P<epg_url_tvg>.*?)"', line)
                    self.epg_url_tvg = result.group('epg_url_tvg') if bool(result) else ''
                    result = re.search('x-tvg-url="(?P<epg_x_tvg_url>.*?)"', line)
                    self.epg_x_tvg_url = result.group('epg_x_tvg_url') if bool(result) else ''
                elif line.startswith(M3U8_CHANNEL_INFO_PREFIX):
                    # Get the Channel Name
                    # Assume for now we MUST always have a ',' so not adding any checking for now
                    details['name'] = line[line.find(',') + 1:]

                    # Get the channel id
                    id_pattern = 'tvg-id="(?P<id>.*?)"'
                    result = re.search(id_pattern, line)
                    details['id'] = result.group('id') if bool(result) else ''

                    # Get the channel Group
                    group_pattern = 'group-title="(?P<group>.*?)"'
                    result = re.search(group_pattern, line)
                    details['group'] = result.group('group') if bool(result) else 'No Group'
                elif line.startswith(M3U8_SPECIAL_LINE_START_TAG):  # If we come here it's unhandled commands, comments, etc
                    pass
                elif not line:  # Empty lines
                    pass
                else:  # Assume it's the url
                    self.add_channel(name=details['name'], url=line, group=details['group'], channel_id=details['id'])
                    details = {}

    def write_file(self, file_path):
        """Write the m3u8 file."""
        self.remove_duplicate_urls()

        with open(file_path, 'w', encoding='utf-8') as file_ptr:
            file_ptr.write(
                F'{M3U8_OPENING_TAG} '
                F'tvg-url="{self.epg_tvg_url}" url-tvg="{self.epg_url_tvg}" x-tvg-url="{self.epg_x_tvg_url}"\n')

            for _, channel_list in self.channel_url_dict.items():
                for channel in channel_list:
                    file_ptr.write(
                        F'''{M3U8_CHANNEL_INFO_PREFIX}0 tvg-id="{channel['id']}" group-title="{channel['group']}"'''
                        F''',{channel["name"]}\n''')
                    file_ptr.write(F'{channel["url"]}\n')


def get_categories_from_json(*, channel_name, json_data):
    """Get the categories for a channel name."""
    categories = []
    for category in json_data:  # pylint: disable=too-many-nested-blocks
        for name, criterias in category.items():
            for criteria in criterias:
                if criteria == 'icontains':
                    for keyword in criterias[criteria]:
                        if keyword.lower() in channel_name.lower():
                            categories.append(name)
                            break
                elif criteria == 'iexact':
                    for keyword in criterias[criteria]:
                        if keyword.lower() == channel_name.lower():
                            categories.append(name)
                            break

    return categories


def remove_meta_data_from_channel_name(name):
    """Remove metadata from channel name e.g. Resolution information etc."""
    channel_name = name

    # Remove anything in brackets
    pattern = re.compile(R'\(.*?\)|\[.*?\]|\{.*?\}', re.IGNORECASE)
    channel_name = re.sub(pattern, ' ', channel_name)

    # Replace Non-Alphanumeric - !!! Must be after any rule using special characters
    channel_name = re.sub('[^0-9a-zA-Z]+', ' ', channel_name)

    # Number Convertion
    sub_pattern_list = [
        ('Eins', '1'), ('Zwei', '2'), ('Drei', '3'), ('Vier', '4'),
        ('I', '1'), ('II', '2'), ('III', '3'), ('IV', '4')
    ]
    search_pattern = ''
    for sub_pattern, replacement in sub_pattern_list:
        search_pattern = F' ({sub_pattern}) |(^{sub_pattern}) | ({sub_pattern}$)'
        pattern = re.compile(search_pattern, re.IGNORECASE)
        channel_name = re.sub(pattern, replacement, channel_name).strip()

    # Remove Misc characters
    sub_pattern_list = ['HD', 'SD', 'FHD', '[2|4]k[+]*', '576|720|1080[p|i]*', 'und',
                        'FS', 'Fernsehen', 'Pluto TV[+]*', 'TV']
    search_pattern = ''
    for sub_pattern in sub_pattern_list:
        search_pattern = F' ({sub_pattern}) |(^{sub_pattern}) | ({sub_pattern}$)'
        pattern = re.compile(search_pattern, re.IGNORECASE)
        channel_name = re.sub(pattern, ' ', channel_name).strip()

    # remove special suffix
    pattern = re.compile('^(.*)tv$', re.IGNORECASE)
    channel_name = re.sub(pattern, R'\1', channel_name.strip())

    # Remove multi spaces inside the string
    pattern = re.compile(R'\s+', re.IGNORECASE)
    channel_name = re.sub(pattern, '', channel_name)

    return channel_name.strip()


def match_epg_channels(m3u8_file, epg_json_path):
    """Match the channels inside the give m3u file object to the channels in the given json file."""
    json_data = {}
    raw_json_data = None
    with open(epg_json_path, 'r') as file_ptr:
        raw_json_data = json.load(file_ptr)

    # Clean up json data
    for info in raw_json_data:
        json_data[remove_meta_data_from_channel_name(info['name']).upper()] = info['tvgid']

    # Find matching channels
    count = 0
    for _, channel_list in m3u8_file.channel_url_dict.items():
        for channel in channel_list:
            channel_name = remove_meta_data_from_channel_name(channel['name'])

            channel_key = channel_name.upper()
            if channel_key in json_data:
                channel['id'] = json_data[channel_key]
                count += 1

    return count


def merge_m3u8_files(*, merge_into_path, merge_from_path):
    """Merge the merge_from_path file into the merge_into_path file."""
    to_file = M3U8File(merge_into_path)
    from_file = M3U8File(merge_from_path)

    to_file.merge(from_file)
    to_file.write_file(merge_into_path)
