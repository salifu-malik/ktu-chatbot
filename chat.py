
import requests
import threading
import json
import google.generativeai as genai
from flask import Flask, render_template, request, jsonify
from data_api import fetch_ktu_data, schedule_weekly_refresh, ktu_data_cache
from apscheduler.schedulers.background import BackgroundScheduler


# Configure Gemini
genai.configure(api_key="AIzaSyDIuN9GrvI2CRvQTl50e0uJVMixsUXktnQ")

# Load static intents
with open("intents.json") as file:
    intents_data = json.load(file)

# Global context variable
context_data = {"text": ""}

def build_context(intents, api_data=None):
    """Build combined context from intents + API data."""
    context = "You are a helpful KTU chatbot. Use the following data to assist users.\n\n"

    # Add intents
    for intent in intents["intents"]:
        context += f"Intent: {intent['tag']}\n"
        context += f"Patterns: {', '.join(intent['patterns'])}\n"
        context += f"Responses: {', '.join(intent['responses'])}\n\n"

    # Add API data if available
    if api_data:
        context += "=== KTU API Data ===\n"
        for key, value in api_data.items():
            context += f"{key}: {value}\n"

    return context

def refresh_ktu_data():
    """Fetches new data from API every week and updates context."""
    try:
        # Example test API (you’ll replace this with your real KTU API later)
        api_url = "https://jsonplaceholder.typicode.com/posts/1"
        response = requests.get(api_url)
        response.raise_for_status()

        api_data = response.json()
        context_data["text"] = build_context(intents_data, api_data)

        print("KTU data refreshed successfully.")
    except Exception as e:
        print(f" Failed to refresh KTU data: {e}")

# Initialize scheduler to refresh every week
scheduler = BackgroundScheduler()
scheduler.add_job(refresh_ktu_data, 'interval', weeks=1)
scheduler.start()

# Run initial fetch in background so Flask can start immediately
threading.Thread(target=refresh_ktu_data).start()

# Set up AI model
model = genai.GenerativeModel("gemini-2.5-flash")

# Flask app setup
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('base.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    user_input = data.get('message', '').strip()
    if not user_input:
        return jsonify({'error': 'No message provided'}), 400

    # Use the latest context
    prompt = f"{context_data['text']}\nUser: {user_input}\nBot:"

    try:
        response = model.generate_content(prompt)
        reply = response.text.strip()
    except Exception as e:
        reply = f"Error: {e}"

    return jsonify({'reply': reply})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
