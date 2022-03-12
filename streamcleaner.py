#!/usr/bin/env python3 -u

import requests
import sys
import m3u8
import argparse
from termcolor import colored
from urllib.parse import urlparse


def parse_arguments():
    p = argparse.ArgumentParser(description='A tool to remove invalid streams from an IPTV playlist file')
    p.add_argument('-i', '--input-file', help='Path to input playlist file', nargs='+', required=True)
    p.add_argument('-o', '--output-file', help='Path to output playlist file')
    p.add_argument('-b', '--blacklist-file', help='Path to blacklist file (one url per line file)', default="")
    p.add_argument('-d', '--debug', help='To enable debug output', action='store_true', default=False)
    p.add_argument('-t', '--timeout', help='URL timeout in seconds', default=1.0, type=float)
    return p.parse_args()


def nice_print(message, colour=None, indent=0, debug=False):
    '''
    Just prints things in colour with consistent indentation
    '''
    if debug and not args.debug:
        return

    if colour == None:
        if 'OK' in message:
            colour = 'green'
        elif 'ERROR' in message:
            colour = 'red'

    print(colored('{0}{1}'.format(' ' * indent * 2, message), colour))


def verify_video_link(url, timeout, indent=1):
    '''
    Verifies a video stream link works
    '''
    nice_print('Loading video: {0}'.format(url), indent=indent, debug=True)

    indent = indent + 1
    parsed_url = urlparse(url)

    if not parsed_url.path.endswith('.ts'):
        nice_print('ERROR unsupported video file: {0}'.format(url))
        return False

    try:
        r = requests.head(url, timeout=(timeout, timeout))
    except Exception as e:
        nice_print('ERROR loading video URL: {0}'.format(str(e)[:100]), indent=indent, debug=True)
        return False
    else:
        video_stream = 'Content-Type' in r.headers and ('video' in r.headers['Content-Type'] or 'octet-stream' in r.headers['Content-Type'])
        if r.status_code != 200:
            nice_print('ERROR {0} video URL'.format(r.status_code, indent=indent, debug=True))
            return False
        elif video_stream:
            nice_print('OK loading video data', indent=indent, debug=True)
            return True
        else:
            nice_print('ERROR unknown URL: {0}'.format(url, indent=indent, debug=True))
            return False


def verify_playlist_link(url, timeout, indent=1, check_first_N_only=5):
    '''
    '''
    nice_print('Loading playlist: {0}'.format(url), indent=indent, debug=True)

    if indent > 6:
        nice_print('ERROR nested playlist too deep', indent=indent)
        return False

    # one nasty server 301-redirected the .m3u8 file to a .mp3 file, ouch. This catches that:
    try:
        m3u8_head = requests.head(url, timeout=(timeout,timeout), allow_redirects=False)
        if 300 <= m3u8_head.status_code < 310:
            m3u8_head2 = requests.head(url, timeout=(timeout,timeout), allow_redirects=True)
            url_redirected=m3u8_head2.history[0].headers['Location']
            extension = urlparse(url_redirected).path.split(".")[-1]
            if extension not in ("m3u8", "m3u"):
                nice_print('ERROR m3u8-playlist 30x-redirected to "{0}"-filetype. Skipping this.'.format(extension), indent=indent, debug=False)
                return False
    except Exception as e:
        nice_print('ERROR loading redirected playlist: {0}'.format(str(e)[:100]), indent=indent, debug=True)
        return False

    try:
        m3u8_obj = m3u8.load(url, timeout=timeout)
    except Exception as e:
        nice_print('ERROR loading playlist: {0}'.format(str(e)[:100]), indent=indent, debug=True)
        return False
    
    if 0 == len(m3u8_obj.data['playlists']) + len(m3u8_obj.data['segments']):
        nice_print('ERROR: playlist is empty.', indent=indent, debug=True)
        return False 

    for nested_playlist in m3u8_obj.data['playlists']:
        if nested_playlist['uri'].startswith(('https://', 'http://')):
            nested_url = nested_playlist['uri']
        else:
            nested_url = '{0}{1}'.format(m3u8_obj.base_uri, nested_playlist['uri'])
        return verify_playlist_link(nested_url, timeout=timeout, indent=indent+1)

    counter=0
    for segment in m3u8_obj.data['segments']:
        if segment['uri'].startswith(('https://', 'http://')):
            url = segment['uri']
        else:
            url = '{0}{1}'.format(m3u8_obj.base_uri, segment['uri'])
            
        if not verify_video_link(url, timeout=timeout):
            return False # first occurring bad one declares this whole list bad. Is that a good choice?
        
        counter+=1
        if counter>=check_first_N_only:
            msg='OK: skipping tests of remaining {0} entries because we have {1} good files already in this playlist'
            nice_print(msg.format(len(m3u8_obj.data['segments'])-counter, counter), indent=indent, debug=True)
            return True

    return True


def verify_playlist_item(item, timeout):
    '''
    Tests playlist url for valid m3u8 data
    '''
    nice_title = item['metadata'].split(',')[-1]
    nice_print('{0} | {1}'.format(nice_title, item['url']), colour='yellow')

    indent = 1

    if item['url'].endswith('.ts'):
        if verify_video_link(item['url'], timeout, indent):
            nice_print('OK video data', indent=indent)
            return True
        else:
            nice_print('ERROR video data', indent=indent)
            return False

    elif item['url'].endswith('.m3u8'):
        if verify_playlist_link(item['url'], timeout, indent):
            nice_print('OK playlist data', indent=indent)
            return True
        else:
            nice_print('ERROR playlist data', indent=indent)
            return False

    else:
        try:
            r = requests.head(item['url'], timeout=(timeout, timeout))
        except Exception as e:
            nice_print('ERROR loading URL: {0}'.format(str(e)[:100]), indent=indent, debug=True)
            return False
        else:
            video_stream = 'Content-Type' in r.headers and ('video' in r.headers['Content-Type'] or 'octet-stream' in r.headers['Content-Type'])
            playlist_link = 'Content-Type' in r.headers and 'x-mpegurl' in r.headers['Content-Type']

            if r.status_code != 200:
                nice_print('ERROR {0} loading URL: {1}'.format(r.status_code, item['url']), indent=indent, debug=True)
                return False
            elif video_stream:
                nice_print('OK loading video data', indent=indent, debug=True)
                return True
            elif playlist_link:
                return verify_playlist_link(item['url'], timeout, indent + 1)
            else:
                nice_print('ERROR unknown URL: {0}'.format(item['url']), indent=indent, debug=True)
                return False


def filter_streams(m3u_files, timeout, blacklist_file):
    '''
    Returns filtered streams from a m3u file as a list
    '''
    blacklist=[]
    if blacklist_file:
        try: 
            with open(blacklist_file) as f:
                content = f.readlines()
                blacklist = [x.strip() for x in content]
        except Exception as e:
            print ("blacklist file issue: {0} {1}" .format(type(e), e))
            sys.exit(1)
        else:
            print ("Successfully loaded {0} blacklisted urls." .format( len(blacklist)))
    
    playlist_items = []
    num_blacklisted=0
        
    for m3u_file in m3u_files:
        try:
            with open(m3u_file) as f:
                content = f.readlines()
                content = [x.strip() for x in content]
        except IsADirectoryError:
            continue

        if content[0] != '#EXTM3U' and content[0].encode("ascii", "ignore").decode("utf-8").strip() != '#EXTM3U':
            raise Exception('Invalid file, no EXTM3U header in "{0}"'.format(m3u_file))

        url_indexes = [i for i, s in enumerate(content) if s.startswith('http')]

        if len(url_indexes) < 1:
            raise Exception('Invalid file, no URLs')

        for u in url_indexes:
            if content[u] in blacklist:
                num_blacklisted+=1
            else:
                detail = {
                    'metadata': content[u - 1],
                    'url': content[u]
                }
                playlist_items.append(detail)
    
    if num_blacklisted:
        print ('Input list already reduced by {0} items, because those urls are on the blacklist.'.format(num_blacklisted))

    print ('Input list now has {0} entries, patience please. Timeout for each test is {1} seconds.'.format(len(playlist_items), timeout))
    filtered_playlist_items = [item for item in playlist_items if verify_playlist_item(item, timeout)]
    print('{0} items filtered out of {1} in total'.format(len(playlist_items) - len(filtered_playlist_items), len(playlist_items)))
    return filtered_playlist_items


if __name__ == '__main__':
    args = parse_arguments()
    
    try:
        filtered_playlist_items = filter_streams(args.input_file, args.timeout, args.blacklist_file)
    except KeyboardInterrupt:
        print('Exiting')
        sys.exit(1)

    if len(filtered_playlist_items) > 0 and args.output_file:
        print('Writing to {0}'.format(args.output_file))
        output_file = open(args.output_file, "w")
        output_file.write('#EXTM3U\n')
        output_file.writelines(['{0}\n{1}\n'.format(item['metadata'], item['url']) for item in filtered_playlist_items])
