#!/bin/bash
# web versions of the cleaned header video: no sound, fast start, 1280x720 for large screens, 854x480 for phones
set -e
S=hero-clean.mp4
ffmpeg -v error -y -i $S -an -c:v libx264 -preset slow -crf 28 -maxrate 1500k -bufsize 3000k -profile:v high -level 4.0 -pix_fmt yuv420p -g 60 -keyint_min 30 -movflags +faststart -vf "scale=1280:720:flags=lanczos" nt-hero-1280.mp4
ffmpeg -v error -y -i $S -an -c:v libx264 -preset slow -crf 28 -maxrate 750k -bufsize 1500k -profile:v main -level 3.1 -pix_fmt yuv420p -g 60 -keyint_min 30 -movflags +faststart -vf "scale=854:480:flags=lanczos" nt-hero-854.mp4
ffmpeg -v error -y -ss 0.4 -i $S -frames:v 1 -q:v 3 poster-1280.jpg
ffmpeg -v error -y -ss 0.4 -i $S -frames:v 1 -vf "scale=854:480:flags=lanczos" -q:v 4 poster-854.jpg
ls -la nt-hero-1280.mp4 nt-hero-854.mp4 poster-1280.jpg poster-854.jpg
# then: copy the two mp4 files to src/files/video/; the poster on the page is the image nt-hero-poster (tools/image_map.json)
