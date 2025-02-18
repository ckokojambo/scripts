from gunicron_spotify_app import app  # Replace 'your_flask_app_file' with the name of your Python file without the .py extension

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3344, debug=True)

