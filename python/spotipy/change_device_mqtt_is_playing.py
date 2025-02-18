import os
import requests
import time
import json
import threading
import paho.mqtt.client as mqtt
from dotenv import load_dotenv
from flask import Flask, request, redirect

# Load environment variables
load_dotenv()

# Spotify API credentials
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = "http://127.0.0.1:3344/callback"

# Spotify API endpoints
AUTH_URL = "https://accounts.spotify.com/authorize"
TOKEN_URL = "https://accounts.spotify.com/api/token"
API_BASE_URL = "https://api.spotify.com/v1"

# MQTT Broker settings
MQTT_BROKER = "mqtt.home.koko"
TOPIC_PRESENCE_KITCHEN = "PRESENCE-kitchen"
TOPIC_PRESENCE2 = "presence2/binary_sensor/presence/state"

# Initialize Flask app
app = Flask(__name__)

# Global variables to store tokens and expiration time
access_token = None
refresh_token = None
token_expires_at = 0
current_device = None  # Track current playback device

# Function to refresh the access token
def refresh_access_token():
    global access_token, refresh_token, token_expires_at

    if not refresh_token:
        raise Exception("No refresh token available.")

    token_data = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    }
    token_response = requests.post(TOKEN_URL, data=token_data)
    token_response_json = token_response.json()

    if "access_token" in token_response_json:
        access_token = token_response_json["access_token"]
        token_expires_at = time.time() + token_response_json.get("expires_in", 3600)
        if "refresh_token" in token_response_json:
            refresh_token = token_response_json["refresh_token"]
        return access_token
    else:
        raise Exception("Failed to refresh access token.")

# Function to check if the access token is expired
def is_token_expired():
    return time.time() >= token_expires_at

# Function to check if music is currently playing
def is_playing():
    global access_token

    if not access_token or is_token_expired():
        try:
            access_token = refresh_access_token()
        except Exception as e:
            print(f"Failed to refresh access token: {e}")
            return False

    headers = {"Authorization": f"Bearer {access_token}"}
    playback_response = requests.get(f"{API_BASE_URL}/me/player", headers=headers)

    if playback_response.status_code == 200:
        playback_data = playback_response.json()
        return playback_data.get("is_playing", False)
    else:
        print(f"Failed to fetch playback state. Status: {playback_response.status_code}")
        return False

# Function to change the playback device
def change_playback_device(device_name):
    global access_token, current_device

    if current_device == device_name:
        print(f"Playback is already on {device_name}. No action taken.")
        return

    if not is_playing():
        print("No song is currently playing. Device change aborted.")
        return

    if not access_token or is_token_expired():
        try:
            access_token = refresh_access_token()
        except Exception as e:
            print(f"Failed to refresh access token: {e}")
            return

    headers = {"Authorization": f"Bearer {access_token}"}
    devices_response = requests.get(f"{API_BASE_URL}/me/player/devices", headers=headers)

    if devices_response.status_code == 200:
        devices = devices_response.json().get("devices", [])
        target_device = next((device for device in devices if device["name"].lower() == device_name.lower()), None)

        if target_device:
            device_id = target_device["id"]
            transfer_data = {"device_ids": [device_id], "play": True}
            transfer_response = requests.put(f"{API_BASE_URL}/me/player", headers=headers, json=transfer_data)

            if transfer_response.status_code == 204:
                current_device = device_name
                print(f"Playback successfully transferred to '{device_name}'.")
            else:
                print(f"Failed to transfer playback. Status: {transfer_response.status_code}")
        else:
            print(f"Device '{device_name}' not found.")
    else:
        print(f"Failed to fetch devices. Status: {devices_response.status_code}")

# MQTT Callbacks
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
        client.subscribe([(TOPIC_PRESENCE_KITCHEN, 0), (TOPIC_PRESENCE2, 0)])
    else:
        print(f"Failed to connect, return code {rc}")

def on_message(client, userdata, msg):
    topic = msg.topic
    payload = msg.payload.decode()

    if topic == TOPIC_PRESENCE_KITCHEN:
        try:
            data = json.loads(payload)
            presence = data.get("presence")
            if presence == 1:
                change_playback_device("kitchen")
        except json.JSONDecodeError:
            print(f"Invalid JSON received on {TOPIC_PRESENCE_KITCHEN}: {payload}")

    elif topic == TOPIC_PRESENCE2:
        if payload == "ON":
            change_playback_device("i5")

# Start MQTT in a separate thread
def start_mqtt():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(MQTT_BROKER, 1883, 60)
    client.loop_forever()

# Start MQTT thread
mqtt_thread = threading.Thread(target=start_mqtt, daemon=True)
mqtt_thread.start()

# Flask Routes
@app.route("/")
def index():
    scope = "playlist-read-private user-read-playback-state user-modify-playback-state"
    auth_params = {
        "client_id": CLIENT_ID,
        "response_type": "code",
        "redirect_uri": REDIRECT_URI,
        "scope": scope,
        "show_dialog": True
    }
    auth_url = f"{AUTH_URL}?{'&'.join([f'{key}={value}' for key, value in auth_params.items()])}"
    return redirect(auth_url)

@app.route("/callback")
def callback():
    global access_token, refresh_token, token_expires_at

    if "error" in request.args:
        return f"Error: {request.args['error']}"

    if "code" in request.args:
        auth_code = request.args["code"]
        token_data = {
            "grant_type": "authorization_code",
            "code": auth_code,
            "redirect_uri": REDIRECT_URI,
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET
        }
        token_response = requests.post(TOKEN_URL, data=token_data)
        token_response_json = token_response.json()

        if "access_token" in token_response_json:
            access_token = token_response_json["access_token"]
            refresh_token = token_response_json["refresh_token"]
            token_expires_at = time.time() + token_response_json.get("expires_in", 3600)
            return "Spotify authentication successful!"
        else:
            return "Failed to retrieve access token."

if __name__ == "__main__":
    app.run(port=3344, debug=True)
