import os
from dotenv import load_dotenv
import subprocess
import time
import threading
import sys
import requests
from currentsong import get_current_playing_song

#Load environment variables
load_dotenv()

commands = ["begin_stream","end_stream", "status_stream", "info_commands_stream","restart_stream","current_song_stream","skip_current_song_stream"]

def control_broadcast(command):
    try:
        if command == "begin_stream":
            return start_stream()
        elif command == "end_stream":
            return stop_stream()
        elif command == "status_stream":
            return get_status_stream()
        elif command == "info_commands_stream":
            return get_info_commands_stream()
        elif command == "restart_stream":
             return restart_stream()
        elif command == "current_song_stream":
             return get_current_song_stream()
        elif command == "skip_current_song_stream":
             return skip_current_song_stream()
    except subprocess.CalledProcessError as e:
        return f"Error controlling Icecast2 server: {e}"

def start_stream():
    subprocess.run(["sudo","systemctl","start","icecast2"], check=True)
    subprocess.run(["ices2","/etc/ices2.xml"], check=True)
    broadcast_ip_address = get_wsl_ip_of_stream()
    return f"Icecast2 server started on http://{broadcast_ip_address}:8000"

def get_wsl_ip_of_stream():
    result = subprocess.run(['./get_wsl_ip.sh'],stdout=subprocess.PIPE)
    ip_address = result.stdout.decode('utf-8').strip()
    return ip_address

def stop_stream():
    subprocess.run(["sudo","systemctl","stop","icecast2"], check=True)
    subprocess.run(["killall","ices2"])
    return "Icecast2 server stopped"

def restart_stream():
    subprocess.run(["sudo","systemctl","restart","icecast2"],check=True)
    subprocess.run(["killall","ices2"])
    subprocess.run(["ices2","/etc/ices2.xml"], check=True)
    return "Icecast2 server has been restarted"

def get_status_stream():
    try:
        result = subprocess.run(["sudo","systemctl","status","icecast2.service"],
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output = result.stdout.decode('utf-8').strip()
        for line in output.splitlines():
            if "Active" in line:
                return f"Icecast2 server is {line.strip()}"
    except subprocess.CalledProcessError as e:
        return f"Failed to get Icecast2 service status: {e}"

def add_song_to_stream(sms_command):
     split_command = sms_command.split()
     youtube_song_url = split_command[1]
     subprocess.run(["./download_audio.sh", youtube_song_url],check=True)
     return f"Song added to playlist. Please restart the stream with 'restart_stream'!"

def skip_current_song_stream():
    subprocess.run(["sudo","killall","-HUP","ices2"],check=True)
    return "Skipping current song... Just wait a second."

def get_current_song_stream():
    current_song = get_current_playing_song()
    print(f"Now playing: {current_song}")

def get_info_commands_stream():
    return (f"Here are the available commands: {commands}\n"
           f"In addition you can use 'add_song_to_stream your-youtube-video-url-here' to add songs to the stream")
if __name__ == "__main__":
    print(f"Welcome to Miros internetradio command line tool! use the command 'info_commands_stream' to see available commands! Quit with CTRL + C")
    while True:
        action = input("Enter command: ")
        sys.stdout.flush()
   # Ensure the input prompt is printed immediately
        if action in commands:
            response = control_broadcast(action)
            print(response)
        elif 'add_song_to_stream' in action:
            response = add_song_to_stream(action)
            print(response)
        else:
            print("Invalid input. Please try again")

        time.sleep(1)
