import re
from pathlib import Path

def get_current_playing_song():
    #the default file path for logs. Check your ices2 config for your path
    log_file_path = '/var/log/ices/ices.log'
    log_file = Path(log_file_path)

    if not log_file.exists():
        return "Error: Log file not found."

    return read_current_song_line_from_log(log_file)

def read_current_song_line_from_log(log_file):
    pattern = r'Currently playing "(.*?)"'
    latest_song = None

    # example line from the log: [2024-10-04  09:56:05] INFO playlist-builtin/playlist_read Currently playing
    #/home/miromuro/linux_palvelimet_projekti/music/Peace Sells (2004 Remaster) [LVhJy-CR64Q].ogg"

    with log_file.open('r') as file:
        #Read from bottom up, for logs are written that way
        for line in reversed(file.readlines()):
            match = re.search(pattern, line)
            if match:
                latest_song = remove_path_and_filename_from_song(match.group(1))
                break

    if latest_song:
        return f"{latest_song}"
    else:
        return "No song information found in the log."

def remove_path_and_filename_from_song(full_path_to_song):
    pattern = r'.*/(.+?)\s*\[[^\]]*\]\.ogg$'
    match = re.search(pattern, full_path_to_song)
    if match:
        return match.group(1)
    return full_path_to_song #Return original string if pattern doesn't match

# Usage
#print(get_current_playing_song())
