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
             return get_stream_info_commands()
        elif sms_command == "restart_stream":
             return restart_icecast2_broadcast()
        elif sms_command == "current_song_stream":
             return get_current_icecast2_song()
        elif sms_command == "skip_current_song_stream":
             return stream_skip_current_song()
        else:
            return f"Invalid command! Use 'info_commands_stream' to get list of current available commands. "
    except subprocess.CalledProcessError as e:
        return f"Error controlling Icecast2 server: {e}"

def start_icecast2_broadcast():
    subprocess.run(["sudo","systemctl","start","icecast2"], check=True)
    subprocess.run(["ices2","/etc/ices2.xml"], check=True)
    return f"Icecast2 server started. Connect to your host machine through the port 8000 and you will be taken to the radio. "

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
    return f"Now playing: {current_song}"

def add_song_to_stream(sms_command):
    print("adding Song to stream")
    split_command_and_url = sms_command.split()
    youtube_song_url = split_command_and_url[1]
    subprocess.run(["./download_audio.sh", youtube_song_url],check=True)
    return f("Song added to playlist. Please restart the broadcast with 'restart_stream'! ")

def get_stream_info_commands():
    commands_info = f"""Stream can be started with 'begin_stream'. Stream can be stopped with 'end_stream'.
    Stream status can be viewed with 'status_stream'. Stream can be restarted with 'restart_stream'. 
    Current song of stream can be displayed with 'current_song_stream'. Current song in stream can be skipped with
    'current_song_stream' A new song to the stream can be appended with 'add_song_to_stream youtube-link-to-song' """
    return commands_info

@app.route("/sms", methods=["POST"])
def incoming_sms():
	"""Handle incoming SMS messages"""
	#Get the message body and senders number
	body = request.values.get("Body","").lower().strip()
	from_number = request.values.get("From","")
	response = "An error occurred while processing your request."
	print("message body: ",body)

	if from_number != user_phone_number:
		response = "Unauthorized phone number"
	if body in ["begin_stream", "end_stream", "status_stream", "info_commands_stream","restart_stream","current_song_stream","skip_current_song_stream"]:
		response = control_broadcast_with_sms(body)
	else:
		response = "Invalid command! Use 'info_commands_stream' to get list of current available commands."
	print("The response", response)
	#Send the response back to the user
	try:
		twiml_response = MessagingResponse()
		print("Twiml res",twiml_response)
		twiml_response.message(response)
		return str(twiml_response)
	except Exception as e:
		print(f"error creating TWiml response: {str(e)}")
		twiml_error = MessagingResponse()
		twiml_error.message("Error creating response")
		return str(twiml_error)
if __name__ == "__main__":
	app.run(host="0.0.0.0", port=5000, debug=True)	
