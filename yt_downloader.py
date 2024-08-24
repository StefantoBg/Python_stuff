#This script is easy yt video downloader, just copy the url and paste it after the script as argument $1
#
import yt_dlp
import sys

# Get the video URL from the command-line argument
if len(sys.argv) > 1:
    video_url = sys.argv[1]
else:
    print("Usage: python down1.py <video_url>")
    sys.exit(1)

# Options for yt-dlp (you can add more if needed)
ydl_opts = {}

# Download the video using yt-dlp
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([video_url])
