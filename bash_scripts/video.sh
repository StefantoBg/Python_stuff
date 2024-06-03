#!/bin/bash

# Check if the file containing URLs is provided
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <file_with_urls>"
    exit 1
fi

# Read the file line by line
while IFS= read -r url; do
    if [ -n "$url" ]; then
        # Run the pytube command with the current URL
        pytube "$url"
    fi
done < "$1"
