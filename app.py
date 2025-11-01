import os
import requests
from flask import Flask, render_template, request, jsonify, send_from_directory
# --- VERCEL PATHING FIX ---
# Get the absolute path of the directory where this file is located
base_dir = os.path.abspath(os.path.dirname(__file__))
# Define the static and template folder paths relative to base_dir
static_folder_path = os.path.join(base_dir, 'static')

app = Flask(__name__, 
            static_folder=static_folder_path, 
            template_folder=static_folder_path) # Point both to the same 'static' dir


# --- CONFIGURATION ---
# We'll get this URL from our n8n workflow later.
# For now, it's a placeholder.
N8N_WEBHOOK_URL = os.environ.get("N8N_WEBHOOK_URL", "http://localhost:5678/webhook-test/b1195e69-c773-4742-affe-d2017a297b66")


@app.route('/')
def index():
    """Serve the main chat page."""
    return render_template('index.html')

@app.route('/<path:path>')
def send_static(path):
    """Serve static files (like CSS, JS) if any."""
    return send_from_directory('static', path)

@app.route('/send_message', methods=['POST'])
def send_message():
    """
    This is the main endpoint for our chat.
    It receives a message from the user, forwards it to our n8n agent,
    and returns the agent's response.
    """
    try:
        user_message = request.json.get('message')
        if not user_message:
            return jsonify({"error": "No message provided"}), 400

        print(f"Received message from user: {user_message}")

        # --- THIS IS WHERE WE TALK TO N8N ---
        # In a real app, we'd send this to our n8n webhook
        # and wait for a proper response.
        
        #
        # try:
        #     # Send data to n8n webhook
        #     n8n_response = requests.post(N8N_WEBHOOK_URL, json={"message": user_message}, timeout=10)
        #     n8n_response.raise_for_status() # Raise an exception for bad status codes
        #
        #     # Get the reply from n8n
        #     # This assumes n8n responds with JSON, e.g., {"reply": "..."}
        #     agent_reply = n8n_response.json().get("reply", "Agent gave an empty response.")
        #
        # except requests.exceptions.RequestException as e:
        #     print(f"Error calling n8n webhook: {e}")
        #     agent_reply = f"Sorry, I couldn't connect to my brain (n8n). Error: {e}"
        #
        #
        
        # --- FOR NOW: We'll just echo the message back for testing ---
        # TODO: Remove this placeholder when n8n is connected.
        if N8N_WEBHOOK_URL == "YOUR_N8N_WEBHOOK_URL_GOES_HERE":
            print("--- N8N NOT CONFIGURED. Echoing message for testing. ---")
            agent_reply = f"ECHO: {user_message}"
        else:
            # This part won't work until the URL is set, but it shows the logic.
            agent_reply = f"Successfully sent to n8n (but this is still a placeholder response)."


        return jsonify({"reply": agent_reply})

    except Exception as e:
        print(f"Error in /send_message: {e}")
        return jsonify({"error": str(e)}), 500

# This is the Vercel entry point
if __name__ == "__main__":
    app.run(debug=True)

