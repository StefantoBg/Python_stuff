#!/usr/bin/env python3

import argparse
from pytube import YouTube


def main():
    parser = argparse.ArgumentParser(description='YouTube Video Downloader using pytube')
    parser.add_argument('url', type=str, help='The URL of the YouTube video to download')
    parser.add_argument('--output_path', type=str, default='.', help='The output path for the downloaded video')
    
    args = parser.parse_args()
    
    download_video(args.url, args.output_path)

def download_video(url, output_path):
    try:
        yt = YouTube(url)
        stream = yt.streams.get_highest_resolution()
        print(f'Downloading: {yt.title}')
        stream.download(output_path)
        print('Download completed!')
    except Exception as e:
        print(f'Error: {e}')

if __name__ == '__main__':
    main()
