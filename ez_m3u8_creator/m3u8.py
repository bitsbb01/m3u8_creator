"""Code to handle m3u8 file type."""

import re

M3U8_OPENING_TAG = '#EXTM3U'
M3U8_CHANNEL_INFO_PREFIX = '#EXTINF:'


class M3U8File():
    """An m3u8 file representation."""

    def __init__(self, file_path=None):
        """Initialize the M3U8 file."""
        self.channel_list = []
        self.epg_tvg_url = ""
        self.epg_url_tvg = ""
        self.epg_x_tvg_url = ""

        if file_path is not None:
            self._load_file(file_path)

    def add_channel(self, *, name, url, group='', channel_id=''):
        """Add a channel to the file."""
        self.channel_list.append({
            'name': name,
            'url': url,
            'group': group,
            'id': channel_id,
        })

    def add_groups_from_category_dic(self, category_dic, *, overwrite=True):
        """Calculate the groups based on the given json file."""
        for channel in self.channel_list:
            categories = get_categories_from_json(channel_name=channel['name'], json_data=category_dic)
            if categories and overwrite:
                channel['group'] = ';'.join(categories)

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
                else:  # Assume it's the url
                    self.add_channel(name=details['name'], url=line, group=details['group'], channel_id=details['id'])
                    details = {}

    def write_file(self, file_path):
        """Write the m3u8 file."""
        with open(file_path, 'w', encoding='utf-8') as file_ptr:
            file_ptr.write(
                F'{M3U8_OPENING_TAG} '
                F'tvg-url="{self.epg_tvg_url}" url-tvg="{self.epg_url_tvg}" x-tvg-url="{self.epg_x_tvg_url}"\n')
            for channel in self.channel_list:
                file_ptr.write(
                    F'''{M3U8_CHANNEL_INFO_PREFIX}0 tvg-id="{channel['id']}" group-title="{channel['group']}"'''
                    F''',{channel["name"]}\n''')
                file_ptr.write(F'{channel["url"]}\n')


def get_categories_from_json(*, channel_name, json_data):
    """Get the categories for a channel name."""
    # if "hr" not in channel_name.lower():
    #     return []

    # print(F'\n\n##### {channel_name} #####')

    categories = []
    for category in json_data:  # pylint: disable=too-many-nested-blocks
        # print('category', category)
        for name, criterias in category.items():
            # print('  name', name)

            for criteria in criterias:
                # print('     criteria', criteria)
                if criteria == 'icontains':
                    for keyword in criterias[criteria]:
                        if keyword.lower() in channel_name.lower():
                            categories.append(name)
                            # print('             => FOUND')
                            break
                elif criteria == 'iexact':
                    # print('CRITERIA', criteria)
                    for keyword in criterias[criteria]:
                        if keyword.lower() == channel_name.lower():
                            categories.append(name)
                            # print('             => FOUND')
                            break

    # print("categories", categories)

    return categories
