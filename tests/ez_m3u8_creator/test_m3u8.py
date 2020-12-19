
from ez_m3u8_creator import m3u8


def test_write_m3u8_file(tmpdir):
    m3u8_file = m3u8.M3U8File()

    m3u8_file.add_channel(name='Channel 1', url='channel_url')
    m3u8_file.add_channel(name='Channel 2', url='channel_url2')

    out_file = tmpdir.join('test.m3u8')
    m3u8_file.write_file(out_file)

    with open(out_file, 'r') as file_ptr:
        line_list = list(file_ptr)
        assert line_list[0].rstrip() == '#EXTM3U'
        assert line_list[1].rstrip() == '#EXTINF:0,Channel 1'
        assert line_list[2].rstrip() == 'channel_url'
        assert line_list[3].rstrip() == '#EXTINF:0,Channel 2'
        assert line_list[4].rstrip() == 'channel_url2'
