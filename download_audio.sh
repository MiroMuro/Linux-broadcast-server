#!/bin/bash

# Check if a  URL is passed as a parameter

if [ -z "$1" ]; then
	echo "Usage: $0 <youtube-link>"
	exit 1
fi

#Check if ffmpeg is installed
if ! command -v ffmpeg &> /dev/null; then
	echo "ffmpeg is not installed. Please install it first."
	exit 1
fi

MUSIC_DIR=/home/$SUDO_USER/linux_palvelimet_projekti/music/

PLAYLIST_DIR=/home/$SUDO_USER/linux_palvelimet_projekti/playlist.txt

MP3_TOTAL_BEFORE_DOWNLOAD=$(find "$MUSIC_DIR" -name "*.mp3" | wc -l)

VIDEO_TITLE=$(yt-dlp --get-title "$1")

echo "Track title: $VIDEO_TITLE \n"

#Run yt-dlp with the passed URL
yt-dlp -x --audio-format mp3 --downloader-args "ffmpeg_i:-update" -P $MUSIC_DIR "$1"

#Check if the yt-dlp command was successful
if [ $? -eq 0 ]; then
	echo "Download completed succefully"
	
	#Find downloaded MP3 file for touch.
	MP3_FILE=$(find "$MUSIC_DIR" -type f -name "$VIDEO_TITLE*.mp3" | tail -n 1)
	echo "DOWNLOADED $MP3_FILE"	
	if [ -n "$MP3_FILE" ]; then
        	echo "Updating modification date of $MP3_FILE to the current date."
        	touch "$MP3_FILE"
    	fi

	MP3_TOTAL_AFTER_DOWNLOAD=$(find "$MUSIC_DIR" -name "*.mp3" | wc -l)
	
	if [ "$MP3_TOTAL_AFTER_DOWNLOAD" -gt "$MP3_TOTAL_BEFORE_DOWNLOAD" ]; then

		#Find the most recently downloaded MP3 file. (The one just touched)
		LATEST_MP3=$(find "$MUSIC_DIR" -name "*.mp3" -type f -printf '%T+ %p\n' | sort -r | head -n 1 | cut -d' ' -f2-)
		if [ -n "$LATEST_MP3" ]; then

			#Generate the OGG filename.
			OGG_FILE="${LATEST_MP3%.mp3}.ogg"

			#Convert MP3 to OGG
			ffmpeg -v verbose -i "$LATEST_MP3" -c:a libvorbis -q:a 4 "$OGG_FILE"
			echo "Converting MP3 to OGG."

			if [ $? -eq 0 ]; then
				#Add new song to Stream playlist.
				echo "Conversion to OGG succesfull: $OGG_FILE"
				echo "Rebuilding playlist..."
				find "$MUSIC_DIR" -name "*.ogg" -type f -exec stat --format="%Y %n" {} + | sort -nr | cut -d' ' -f2- > "$PLAYLIST_DIR"
				echo "Playlist rebuilt with new song."
			else
				echo "Conversion to OGG failed"
			fi
		else
			echo "No MP3 file found to convert."
		fi	
	else
		echo "No new MP3 file was downloaded."
	fi
else
	echo "Download failed. Please check the URL or the internet connection."
fi
