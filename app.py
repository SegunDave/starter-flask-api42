from flask import Flask, jsonify
import threading
import time
from supabase import create_client
import api  # This module should contain your Supabase URL and API key

app = Flask(__name__)

# Initialize the Supabase client
supabase = create_client(api.url, api.key)

# Store the current Wi-Fi signal strength
current_signal_strength = {'strength': '1'}

def fetch_signal_strength():
    while True:
        data, error = supabase.table('controller_commands').select('*').order('time', desc=True).limit(1).execute()
        if data:
            command = data[1][0]['command']
            current_signal_strength['strength'] = command
        else:
            # handle error
            time.sleep(1)

# Start a background thread to update the Wi-Fi signal strength
thread = threading.Thread(target=fetch_signal_strength)
thread.daemon = True
thread.start()

@app.route('/wifi-signal')
def wifi_signal():
    return jsonify(current_signal_strength)
