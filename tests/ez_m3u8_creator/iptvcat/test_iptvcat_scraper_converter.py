
import os
import pytest

from ez_m3u8_creator.iptvcat import iptvcat_scraper_converter


TEST_FILE_INTEGRATION_PATH = R'tests/ez_m3u8_creator/TestFiles/test_file_integration.json'
TEST_FILE_INTEGRATION_CONVERTED_PATH = R'tests/ez_m3u8_creator/TestFiles/test_file_integration_converted.m3u8'
TEST_PATH_DIR = R'tests/ez_m3u8_creator/TestFiles/TestFolder'

def test_parse_json_file():
    file_path = TEST_FILE_INTEGRATION_PATH
    iptvcat_file = iptvcat_scraper_converter.IptvCatFile(file_path)

    assert iptvcat_file.path == file_path

    expected_ids = ['1', '2', '3', '4', '5']
    assert len(iptvcat_file) == len(expected_ids)

    imported_ids = [d['id'] for d in iptvcat_file]
    assert sorted(imported_ids) == sorted(expected_ids)

FILTER_IDS = [
    (TEST_FILE_INTEGRATION_PATH, ['INVALID_STATUS'], 0, []),
    (TEST_FILE_INTEGRATION_PATH, ['INVALID_STATUS'], 100, []),
    (TEST_FILE_INTEGRATION_PATH, ['online'], 100, ['2', '5']),
    (TEST_FILE_INTEGRATION_PATH, ['online'], 99, ['2', '3', '5']),
    (TEST_FILE_INTEGRATION_PATH, ['online'], 0, ['1', '2', '3', '5']),
    (TEST_FILE_INTEGRATION_PATH, ['offline'], 0, ['4']),
]
@pytest.mark.parametrize('file_path, status_list, liveliness, expected_ids', FILTER_IDS)
def test_filter_channel_list(file_path, status_list, liveliness, expected_ids):
    iptvcat_file = iptvcat_scraper_converter.IptvCatFile(file_path)

    iptvcat_file.filter_channels(status_list=status_list, liveliness_min=liveliness)
    ids = [d['id'] for d in iptvcat_file]
    assert sorted(ids) == sorted(expected_ids)


def test_convert_json_to_m3u8(tmpdir):
    out_file = tmpdir.join('output.m3u8')

    file_path = TEST_FILE_INTEGRATION_PATH
    converted_file_path = TEST_FILE_INTEGRATION_CONVERTED_PATH
    iptvcat_file = iptvcat_scraper_converter.IptvCatFile(file_path)
    iptvcat_file.filter_channels(status_list=['online'], liveliness_min=100)

    iptvcat_file.write_playlist(out_path=out_file)

    with open(converted_file_path, 'r', encoding='utf-8') as file_ptr:
        in_file_line_list = list(file_ptr)
        out_file_line_list = out_file.read_text(encoding='utf-8').split('\n')

        assert len(in_file_line_list) == 5

        # Rough test that all the lines are matching
        for idx, line in enumerate(in_file_line_list):
            assert line.rstrip() == out_file_line_list[idx]


def test_convert_dir_to_m3u8(tmpdir):
    convert_dir = TEST_PATH_DIR

    iptvcat_scraper_converter.convert_json_dir_to_m3u8(in_dir=convert_dir, out_dir=tmpdir)

    for root, _, files in os.walk(convert_dir):
        for filename in files:
            if not filename.lower().endswith('.json'):
                continue

            converted_file_name = os.path.splitext(filename)[0] + '.m3u8'
            converted_file_path = os.path.join(tmpdir, converted_file_name)
            test_file_path = os.path.join(convert_dir, converted_file_name)

            print('test_file_path', test_file_path)
            print('converted_file_path', converted_file_path)

            assert os.path.exists(test_file_path)
            assert os.path.exists(converted_file_path)

            with open(converted_file_path, 'r', encoding='utf-8') as convert_file_ptr:
                with open(test_file_path, 'r', encoding='utf-8') as test_file_ptr:
                    convert_file_list = list(convert_file_ptr)
                    test_file_list = list(test_file_ptr)

                    print('Converted Lines', convert_file_list)
                    print('Test File Lines', test_file_list)
                    assert len(convert_file_list) == len(test_file_list)

                    for idx, line in enumerate(convert_file_list):
                        assert line == test_file_list[idx]
