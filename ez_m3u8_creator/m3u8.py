"""Code to handle m3u8 file type."""

M3U8_OPENING_TAG = '#EXTM3U'
M3U8_CHANNEL_INFO_PREFIX = '#EXTINF:0'


class M3U8File():
    """An m3u8 file representation."""

    def __init__(self):
        """Initialize the M3U8 file."""
        self.channel_list = []

    def add_channel(self, *, name, url):
        """Add a channel to the file."""
        self.channel_list.append({
            'name': name,
            'url': url
        })

    def write_file(self, file_path):
        """Write the m3u8 file."""
        with open(file_path, 'w', encoding='utf-8') as file_ptr:
            file_ptr.write(F'{M3U8_OPENING_TAG}\n')
            for channel in self.channel_list:
                file_ptr.write(F'{M3U8_CHANNEL_INFO_PREFIX},{channel["name"]}\n')
                file_ptr.write(F'{channel["url"]}\n')
