# Python Icecast2 Broadcast Server with SMS Input

This project is an Icecast2 broadcast server with Ices2 as the streaming source, featuring SMS input capabilities via Twilio and Flask. It's designed to run on WSL2 and is exposed to the internet using ngrok.

## Features

- Icecast2 broadcast server
- Ices2 streaming source
- SMS input capabilities using Twilio
- Web interface with Flask
- Internet exposure via ngrok
- Youtube download capabilities with yt-dlp

## Requirements

- Python 3.x
- WSL2 (Windows Subsystem for Linux 2)
- Icecast2
- Ices2
- ngrok
- yt-dlp

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/MiroMuro/Linux-broadcast-server.git
   cd linux-broadcast-server
   ```

2. Set up a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Set up your environment variables in a `.env` file (see Configuration section).

## Configuration

Create a `.env` file in the project root with the following variables:

```
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=your_host

TWILIO_ACCOUNT_SID=your_twilio_account_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_PHONE_NUMBER=your_twilio_phone_number
FLASK_SECRET_KEY=your_flask_secret_key
```

## Setting up required packages
## Icecast2

1. Update your package list:
   ```
   sudo apt update
   ```
2. Install Icecast2:
   ```
   sudo apt install icecast2
   ```
3. During installation, you'll be prompted to configure Icecast2. You can choose to configure it now or later.
4. Edit the Icecast configuration file:
   ```
   sudo nano /etc/icecast2/icecast.xml
   ```
5. Modify the necessary settings such as passwords, hostname, and ports.
6. Start Icecast2:
   ```
   sudo service icecast2 start
   ```
7. You can now access the broadcast with a browser from the host and port configured in icecast.xml

### Ices2

1. Install Ices2:
   ```
   sudo apt install ices2
   ```

2. Edit the configuration file for ices2:
   ```
   sudo nano /etc/ices2.xml
   ```

3. Configure the file according to your needs, including the connection to your Icecast2 server and path to the playlist.txt in this projects root folder

4. Start Ices2:
   ```
   ices2 /etc/ices2.xml
   ```

3. Run the Ices2 source client.
4. Start the Flask application:
   ```
   python app.py
   ```

5. Start ngrok to expose your local server:
   ```
   ngrok http 5000
   ```
### ngrok

1. Download ngrok (pick a distribution suitable to your computer):
   ```
   wget https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-amd64.zip
   ```

2. Unzip the downloaded file:
   ```
   unzip ngrok-stable-linux-amd64.zip
   ```

3. Move ngrok to a location in your PATH:
   ```
   sudo mv ngrok /usr/local/bin
   ```

4. Sign up for a free ngrok account and get your authtoken.

5. Configure ngrok with your authtoken:
   ```
   ngrok authtoken YOUR_AUTH_TOKEN
   ```
### yt-dlp

1. Install yt-dlp:
   ```
   sudo curl -L https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp -o /usr/local/bin/yt-dlp
   sudo chmod a+rx /usr/local/bin/yt-dlp
   ```

2. Test the installation:
   ```
   yt-dlp --version
   ```
## ffmpeg
1. Install ffmpeg video and audio convertion software
   ```
   sudo apt install ffmpeg
   ```
## Usage
## Twilio app
1. Activate the venv in the projects root folder
```
source venv/bin/activate
```
2. Run the app as Sudo with the venv's python
```
sudo ./venv/bin/python twilio_app.py
```
The Icecast2 server will run on default port 8000 and the Flask app for twilio will run on port 5000 as default.
3. Open up another WSL2-instance and activate the previously installed ngrok on port 5000
```
ngrok http 5000
```
4. Grab the ngrok-generated ip address
![kuva](https://github.com/user-attachments/assets/a8f89d77-dc4e-4263-b4e2-a2530fb52910)
5. Add the ngrok-generated ip address to your phone that you got from twilio. This can be done on twilios website after logging in. Dont forget to the /sms endpoint at the end.
![kuva](https://github.com/user-attachments/assets/fd5780ab-2fa0-4f62-8186-96755f328b54)

6. The app is running! Text your twilio phone number "info_commands_stream" to get the available commands.
![Screenshot_20241009-161643](https://github.com/user-attachments/assets/d7062f8b-3efe-46af-a72c-f0d25e1e086d)
7. After texting "begin_stream" the sites shows up at http://your-wsl2-ip-address:8000
![kuva](https://github.com/user-attachments/assets/0c883991-4293-411f-aad7-8360c676dca0)

## Command line app

## Contact

Miro Laukkanen - miro.laukkanen44@gmail.com


