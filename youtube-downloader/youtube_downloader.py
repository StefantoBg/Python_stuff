#!/usr/bin/env python3
import argparse
from pytube import YouTube, Playlist
import time
import os

def main():
    parser = argparse.ArgumentParser(description='YouTube Video Downloader using pytube')
    parser.add_argument('url', type=str, help='The URL of the YouTube video or playlist to download')
    parser.add_argument('--output_path', type=str, default='.', help='The output path for the downloaded video(s)')
    parser.add_argument('--playlist', action='store_true', help='Indicates that the URL is a playlist')
    parser.add_argument('--mp3', action='store_true', help='Download playlist in MP3 format (default is MP4)')

    args = parser.parse_args()

    if args.playlist:
        download_playlist(args.url, args.output_path, mp3=args.mp3)
    else:
        download_video(args.url, args.output_path, mp3=args.mp3)

def download_video(url, output_path, retries=3, mp3=False):
    for attempt in range(retries):
        try:
            yt = YouTube(url)

            if mp3:
                stream = yt.streams.filter(only_audio=True).first()
                file_extension = 'mp3'
            else:
                stream = yt.streams.filter(adaptive=True, file_extension='mp4').first()
                file_extension = 'mp4'

            if stream:
                print(f'Downloading: {yt.title} ({stream.resolution}, {stream.mime_type})')
                filename = f"{yt.title}.{file_extension}"
                stream.download(output_path, filename=filename)
                print('Download completed!')
                return True
            else:
                print(f"No suitable {file_extension.upper()} stream found for {yt.title}")
                return False

        except Exception as e:
            print(f'Error: {e}')
            if attempt < retries - 1:
                print(f'Retrying... ({attempt + 1}/{retries})')
                time.sleep(5)  # Wait for 5 seconds before retrying
            else:
                print('Failed to download video after several attempts.')
                return False
        time.sleep(5)  # Add a delay before retrying

def download_playlist(url, output_path, retries=3, mp3=False):
    try:
        pl = Playlist(url)
        print(f'Downloading playlist: {pl.title}')
        for video in pl.videos:
            success = download_video(video.watch_url, output_path, retries, mp3=mp3)
            if not success:
                print(f'Skipped video: {video.title}')
        print('Playlist download completed!')
    except Exception as e:
        print(f'Error: {e}')

if __name__ == '__main__':
    main()


