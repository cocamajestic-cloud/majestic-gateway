from flask import Flask, request, jsonify
import json
import os
import openai
from flask_cors import CORS

app = Flask(__name__)

# For initial testing, allow all origins (change this to your domain once confirmed)
CORS(app)

# Load persona from file once at startup
with open("persona.json", "r") as f:
    persona = json.load(f)

# Set OpenAI API key from environment variable on Render
openai.api_key = os.environ.get("OPENAI_API_KEY")

@app.route("/")
def home():
    return f"{persona['name']} is online."

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "")

    # Build prompt using persona data and user input
    prompt = f"""
You are {persona['role']}.
Tone: {persona['tone']}.
Constraints: {persona['constraints']}.
User says: {user_message}
"""

    try:
        # Call OpenAI API to get chat completion
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Change if needed
            messages=[{"role": "system", "content": prompt}],
            max_tokens=250,
            temperature=0.7
        )
        reply = response.choices[0].message["content"].strip()
    except Exception as e:
        # Return error message as JSON
        return jsonify({"error": str(e)}), 500

    return jsonify({"reply": reply})

if __name__ == "__main__":
    # Bind to all interfaces on port 5000 for Render
    app.run(host="0.0.0.0", port=5000)
