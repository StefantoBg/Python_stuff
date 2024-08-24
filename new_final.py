import yt_dlp
import sys
import re

# Get the video URL, time frame, resolution, and output file name from command-line arguments
if len(sys.argv) < 2:
    print("Usage: python script.py <video_url> --cliptime <start-end> --resolution <low|medium|high> --output <filename>")
    sys.exit(1)

video_url = sys.argv[1]

# Default values
start_time = None
end_time = None
resolution = 'high'  # Default to high resolution
output_name = None  # Default to no specific output name

# Extract time range if provided (in seconds, e.g., --cliptime 12-233)
if "--cliptime" in sys.argv:
    try:
        clip_arg_index = sys.argv.index("--cliptime")
        cliptime = sys.argv[clip_arg_index + 1]
        start_time, end_time = map(int, re.split(r'[-:]', cliptime))
    except (ValueError, IndexError):
        print("Invalid time format. Use: --cliptime <start-end> (e.g., 12-233 in seconds)")
        sys.exit(1)

# Extract resolution if provided (e.g., --resolution low|medium|high)
if "--resolution" in sys.argv:
    try:
        resolution_arg_index = sys.argv.index("--resolution")
        resolution = sys.argv[resolution_arg_index + 1].lower()
    except (ValueError, IndexError):
        print("Invalid resolution format. Use: --resolution <low|medium|high>")
        sys.exit(1)

# Extract output file name if provided (e.g., --output filename.mp4)
if "--output" in sys.argv:
    try:
        output_arg_index = sys.argv.index("--output")
        output_name = sys.argv[output_arg_index + 1]
    except (ValueError, IndexError):
        print("Invalid output format. Use: --output <filename>")
        sys.exit(1)

# Set resolution filters for yt-dlp
resolution_map = {
    'low': 'bestvideo[height<=144]+bestaudio/best',
    'medium': 'bestvideo[height<=360]+bestaudio/best',
    'high': 'bestvideo[height<=1080]+bestaudio/best'
}

ydl_opts = {
    'format': resolution_map[resolution],  # Set format based on user input
    'outtmpl': output_name if output_name else '%(title)s.%(ext)s',  # Set output template
    'recode-video': 'mp4'  # Force the output format to be mp4
}

# Add postprocessor options if time frame is specified
if start_time is not None and end_time is not None:
    ydl_opts['postprocessor_args'] = [
        '-ss', str(start_time),
        '-to', str(end_time)
    ]

# Download the specified portion of the video in the desired resolution
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([video_url])
