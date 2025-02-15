import os
import base64
import requests
from dotenv import load_dotenv
from flask import Flask, request, redirect

# Load environment variables
load_dotenv()

# Spotify API credentials
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")

# Spotify API endpoints
AUTH_URL = "https://accounts.spotify.com/authorize"
TOKEN_URL = "https://accounts.spotify.com/api/token"
API_BASE_URL = "https://api.spotify.com/v1"

# Initialize Flask app
app = Flask(__name__)

# Step 1: Redirect user to Spotify authorization page
@app.route("/")
def index():
    # Define the scope of access (playlist read access)
    scope = "playlist-read-private"

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
            return redirect(f"/playlists?access_token={access_token}")
        else:
            return "Failed to retrieve access token."

# Step 3: Fetch and display the user's playlists
@app.route("/playlists")
def get_playlists():
    # Get the access token from the query parameters
    access_token = request.args.get("access_token")

    if not access_token:
        return "Access token missing."

    # Fetch the user's playlists
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    playlists_response = requests.get(f"{API_BASE_URL}/me/playlists", headers=headers)
    playlists_response_json = playlists_response.json()

    if "items" in playlists_response_json:
        playlists = playlists_response_json["items"]
        playlist_names = [playlist["name"] for playlist in playlists]
        return f"Your Playlists: {', '.join(playlist_names)}"
    else:
        return "No playlists found or an error occurred."

# Run the Flask app
if __name__ == "__main__":
    app.run(port=3344, debug=True)
