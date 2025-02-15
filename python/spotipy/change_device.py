import os
import requests
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

# Initialize Flask app
app = Flask(__name__)

# Step 1: Redirect user to Spotify authorization page
@app.route("/")
def index():
    # Define the scope of access (playback and device control)
    scope = "playlist-read-private user-read-playback-state user-modify-playback-state"

    # Redirect user to Spotify authorization page
    auth_params = {
        "client_id": CLIENT_ID,
        "response_type": "code",
        "redirect_uri": REDIRECT_URI,
        "scope": scope,
        "show_dialog": True  # Optional: Force user to re-authenticate
    }
    auth_url = f"{AUTH_URL}?{'&'.join([f'{key}={value}' for key, value in auth_params.items()])}"
    return redirect(auth_url)

# Step 2: Handle the callback from Spotify
@app.route("/callback")
def callback():
    # Check for errors in the callback
    if "error" in request.args:
        return f"Error: {request.args['error']}"

    # Exchange the authorization code for an access token
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
            return redirect(f"/change-device?access_token={access_token}")
        else:
            return "Failed to retrieve access token."

# Step 3: Change the playback device to "kitchen"
@app.route("/change-device")
def change_device():
    # Get the access token from the query parameters
    access_token = request.args.get("access_token")

    if not access_token:
        return "Access token missing."

    # Fetch the current playback devices
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    devices_response = requests.get(f"{API_BASE_URL}/me/player/devices", headers=headers)

    if devices_response.status_code == 200:
        devices = devices_response.json().get("devices", [])
        if devices:
            # Find the device ID for "kitchen"
            kitchen_device = next((device for device in devices if device["name"].lower() == "kitchen"), None)
            if kitchen_device:
                device_id = kitchen_device["id"]
                # Transfer playback to "kitchen"
                transfer_url = f"{API_BASE_URL}/me/player"
                transfer_data = {
                    "device_ids": [device_id],
                    "play": True  # Optional: Start playback on the new device
                }
                transfer_response = requests.put(transfer_url, headers=headers, json=transfer_data)

                if transfer_response.status_code == 204:
                    return "Playback successfully transferred to 'kitchen'."
                else:
                    return f"Failed to transfer playback. Status code: {transfer_response.status_code}"
            else:
                return "Device 'kitchen' not found."
        else:
            return "No active playback devices found."
    else:
        return f"Failed to fetch devices. Status code: {devices_response.status_code}"

# Run the Flask app
if __name__ == "__main__":
    app.run(port=3344, debug=True)
