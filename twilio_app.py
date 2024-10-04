import os
from flask import Flask, request
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
from dotenv import load_dotenv
import subprocess
import time
import threading
import sys
import requests
from currentsong import get_current_playing_song
#Load environment variables
load_dotenv()

#Twilio credentials
account_ssid=os.getenv('TWILIO_ACC_SID')
auth_token=os.getenv('TWILIO_AUTH_TOKEN')
twilio_phone_number=os.getenv('TWILIO_PHONE_NUMBER')
user_phone_number=os.getenv("USER_PHONE_NUMBER")


#Initialize Twilio client
twilio_client = Client(account_ssid ,auth_token)

#Initialize flask app
app = Flask(__name__)

def control_broadcast_with_sms(sms_command):
    try:
        if sms_command == "begin_stream":
            return start_icecast2_broadcast()
        elif sms_command == "end_stream":
            return stop_icecast2_broadcast()
        elif sms_command == "status_stream":
            return get_icecast2_service_status()
        elif sms_command == "info_commands_stream":
            return f"Stream can be started with 'begin_stream'. Stream can be stopped with 'end_stream'. Stream status can be viewed with 'status_stream'."
        elif sms_command == "restart_stream":
             return restart_icecast2_broadcast()
        elif sms_command == "current_song_stream":
             return get_current_icecast2_song()
        elif sms_command == "skip_current_song_stream":
             return stream_skip_current_song()
        else:
            return f"Invalid actions! Use 'begin_stream', 'end_stream' or 'status_stream'"
    except subprocess.CalledProcessError as e:
        return f"Error controlling Icecast2 server: {e}"

def start_icecast2_broadcast():
    subprocess.run(["sudo","systemctl","start","icecast2"], check=True)
    subprocess.run(["ices2","/etc/ices2.xml"], check=True)
    broadcast_ip_address = get_wsl_ip_of_broadcast()
    return f"Icecast2 server started on http://{broadcast_ip_address}:8000"

def get_wsl_ip_of_broadcast():
    result = subprocess.run(['./get_wsl_ip.sh'],stdout=subprocess.PIPE)
    ip_address = result.stdout.decode('utf-8').strip()
    return ip_address

def stop_icecast2_broadcast():
    subprocess.run(["sudo","systemctl","stop","icecast2"], check=True)
    return "Icecast2 server stopped"

def get_icecast2_service_status():
    try:
        result = subprocess.run(["sudo","systemctl","status","icecast2.service"],
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output = result.stdout.decode('utf-8').strip()
        for line in output.splitlines():
            if "Active" in line:
                return f"Icecast2 server is {line.strip()}"
    except subprocess.CalledProcessError as e:
        return f"Failed to get Icecast2 service status: {e}"

def restart_icecast2_broadcast():
    subprocess.run(["sudo","systemctl","restart","icecast2"],check=True)
    subprocess.run(["killall","ices2"])
    subprocess.run(["ices2","/etc/ices2.xml"], check=True)
    return "icecast2 server has been restarted"

def stream_skip_current_song():
    subprocess.run(["sudo","killall","-HUP","ices2"],check=True)
    return "Skipping current song... just wait a second"

def get_current_icecast2_song():
    current_song = get_current_playing_song()
    print(f"Now playing: {current_song}")

def add_song_to_stream(sms_command):
    split_command_and_url = sms_command.split()
    youtube_song_url = split_command_and_url[1]
    subprocess.run(["./download_audio.sh", youtube_song_url],check=True)
    return f("Song added to playlist. Please restart the broadcast with 'restart_stream'! ")

@app.route("/sms", methods=["POST"])
def incoming_sms():
	"""Handle incoming SMS messages"""
	#Get the message body and senders number
	body = request.values.get("Body","").lower().strip()
	from_number = request.values.get("From","")

	if from_number != user_phone_number:
		response = "Unauthorized phone number"
        if body in ["begin_stream", "end_stream", "status_stream", "info_commands_stream","stream_restart","stream_current_song","stream_skip_song"]:
            response = control_broadcast_with_sms(body)
        elif "add_song_to_stream" in body
            response = add_song_to_stream(body)
	else:
		response = "Invalid input. Please try again."

	#Send the response back to the user
	twiml_response = MessagingResponse()
	twiml_response.message(response)
	return str(twiml_response)

if __name__ == "__main__":
	app.run(host="0.0.0.0", port=5000, debug=True)	
