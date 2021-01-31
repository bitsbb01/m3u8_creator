
import pytest

from ez_m3u8_creator import m3u8

TEST_FILE_CONVERTION_TEST = R'tests/ez_m3u8_creator/TestFiles/test_file_convertion_test.m3u8'

EPG_GERMAN_JSON_PATH = R'ez_m3u8_creator/m3u4u.com/egp-channel-ids/germany.json'


def test_write_m3u8_file(tmpdir):
    m3u8_file = m3u8.M3U8File()

    m3u8_file.add_channel(name='Channel 1', url='channel_url', group='Sport')
    m3u8_file.add_channel(name='Channel 2', url='channel_url2', channel_id='MyD.com')

    out_file = tmpdir.join('test.m3u8')
    m3u8_file.write_file(out_file)

    with open(out_file, 'r') as file_ptr:
        line_list = list(file_ptr)
        assert line_list[0].rstrip() == '#EXTM3U tvg-url="" url-tvg="" x-tvg-url=""'
        assert line_list[1].rstrip() == '#EXTINF:0 tvg-id="" group-title="Sport",Channel 1'
        assert line_list[2].rstrip() == 'channel_url'
        assert line_list[3].rstrip() == '#EXTINF:0 tvg-id="MyD.com" group-title="",Channel 2'
        assert line_list[4].rstrip() == 'channel_url2'


def test_load_m3u8_file(tmpdir):
    m3u8_file = m3u8.M3U8File(TEST_FILE_CONVERTION_TEST)
    
    out_file = tmpdir.join('output.m3u8')
    m3u8_file.write_file(out_file)

    with open(TEST_FILE_CONVERTION_TEST, 'r', encoding='utf-8') as file_ptr:
        in_file_line_list = [x.rstrip() for x in list(file_ptr)]
        out_file_line_list = out_file.read_text(encoding='utf-8').split('\n')

        print('Test File ', in_file_line_list)
        print('Check File', out_file_line_list)

        # Ensure there are at least some lines in the file
        assert len(in_file_line_list) > 3

        # Rough test that all the lines are matching
        for idx, line in enumerate(in_file_line_list):
            assert line == out_file_line_list[idx]


TEST_JSON_CATEGORIES = [
    {
        'News': {
            'icontains': ['cnn', 'cnbc', 'bbc']
        },
    },
    {
        'Sport': {
            'icontains': ['sport'],
            'iexact': ['TestMe'],
        }
}]
CHANNEL_CATEGORIES = [
    ('CNBC', ['News']),
    ('sPort', ['Sport']),
    ('CNN SPORT', ['News', 'Sport']),
    ('Sport 1', ['Sport']),
    ('RTL II', []),
    ('TestMe Not', []),
    ('TestMe', ['Sport']),
]
@pytest.mark.parametrize('channel_name, category_list', CHANNEL_CATEGORIES)
def test_get_categories_from_json(channel_name, category_list):
    assert category_list == m3u8.get_categories_from_json(channel_name=channel_name, json_data=TEST_JSON_CATEGORIES)


def test_add_categories_from_json_to_m3u():
    category_dic = [
    {
        'News': {
            'icontains': ['cnn', 'cnbc', 'bbc']
        },
    },
    {
        'Sport': {
            'icontains': ['sport']
        },
    },
    ]

    m3u8_file = m3u8.M3U8File()

    m3u8_file.add_channel(name='CNN Sport', url='channel_url')

    assert m3u8_file.channel_url_dict['channel_url'][0]['name'] == 'CNN Sport'
    assert m3u8_file.channel_url_dict['channel_url'][0]['group'] == ''

    m3u8_file.add_groups_from_category_dic(category_dic, overwrite=False)
    assert m3u8_file.channel_url_dict['channel_url'][0]['group'] == ''

    m3u8_file.add_groups_from_category_dic(category_dic)
    assert m3u8_file.channel_url_dict['channel_url'][0]['group'] == 'News;Sport'


def test_remove_duplicate_urls():
    m3u8_file = m3u8.M3U8File()

    m3u8_file.add_channel(name='Channel 1', url='channel_url_1')
    m3u8_file.add_channel(name='Channel 2', url='channel_url_2')
    m3u8_file.add_channel(name='Channel 1', url='channel_url_1')

    assert len(m3u8_file.channel_url_dict) == 2
    assert len(m3u8_file.channel_url_dict['channel_url_1']) == 2
    assert len(m3u8_file.channel_url_dict['channel_url_2']) == 1

    m3u8_file.remove_duplicate_urls()
    assert len(m3u8_file.channel_url_dict) == 2
    assert len(m3u8_file.channel_url_dict['channel_url_1']) == 1
    assert len(m3u8_file.channel_url_dict['channel_url_2']) == 1


GERMAN_CHANNEL_EPG_MAPPING = [
    ('ZDF', 'ZDF.de'),
    ('ZDF ', 'ZDF.de'),
    ('  ZDF  ', 'ZDF.de'),
    (' ZDF', 'ZDF.de'),
    ('ZDF HD', 'ZDF.de'),
    ('ZDF hD', 'ZDF.de'),
    ('ZDF SD', 'ZDF.de'),
    ('ZDF FHD', 'ZDF.de'),
    ('ZDF 4K', 'ZDF.de'),
    ('ZDF 4k', 'ZDF.de'),
    ('ZDF 4K+', 'ZDF.de'),
    ('ZDF (HD)', 'ZDF.de'),
    ('ZDF (720)', 'ZDF.de'),
    ('ZDF(HD)', 'ZDF.de'),
    ('(HD)ZDF', 'ZDF.de'),
    ('(HD)ZDF(720)', 'ZDF.de'),
    ('ZDF.tv', 'ZDF.de'),
    ('3-SAT', '3sat.de'),

    ('SKY SPORT NEWS', 'SkySportNews.de'),
    ('SKY SPORT HD NEWS', 'SkySportNews.de'),
    ('Dresden Fernsehen', 'DresdenFernsehen.de'),
    ('Auto Motor Sport', 'AutoMotorSport.de'),
    ('Auto Motor und Sport', 'AutoMotorSport.de'),
    ('Auto Motor & Sport', 'AutoMotorSport.de'),
    ('E! ENTERTAINMENT FHD', 'EEntertainment.de'),
    ('NDR Fernsehen', 'NDR(src02).de'),
    ('NDR FS', 'NDR(src02).de'),
    ('Pluto TV Fight', 'PlutoTVFight(English).de'),
    ('Pluto TV+ Fight', 'PlutoTVFight(English).de'),
    ('1-2-3 TV HD', '123tv.de'),

    ('Bremen Eins', 'BremenEins.de'),
    ('Bremen zwei', 'BremenZwei.de'),
    #('Bremen DREI', ''),  # No Channel for Test
    ('Bremen Vier', 'BremenVier.de'),
    ('Bremen I', 'BremenEins.de'),
    ('Bremen II', 'BremenZwei.de'),
    #('Bremen III', ''),  # No Channel for Test
    ('Bremen IV', 'BremenVier.de'),
]
@pytest.mark.parametrize('name, epg', GERMAN_CHANNEL_EPG_MAPPING)
def test_match_german_channels_to_epg(name, epg):
    url = F'http://{name}'

    m3u8_file = m3u8.M3U8File()
    m3u8_file.add_channel(name=name, url=url)

    m3u8.match_epg_channels(m3u8_file, EPG_GERMAN_JSON_PATH)

    assert m3u8_file.channel_url_dict[url][0]['id'] == epg
