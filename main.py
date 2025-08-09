from flask import Flask, request, jsonify
import json
import os
import openai

app = Flask(__name__)

# Load personas from file
with open("personas.json", "r") as f:
    PERSONAS = json.load(f)

# Set your OpenAI API key from Render environment variable
openai.api_key = os.environ.get("OPENAI_API_KEY")

@app.route("/")
def home():
    return "Chatbot backend is running."

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    bot_name = data.get("bot", "oberon").lower()
    user_message = data.get("message", "")

    if bot_name not in PERSONAS:
        return jsonify({"error": "Bot not found"}), 404

    persona = PERSONAS[bot_name]
    prompt = f"""
    You are {persona['role']}.
    Tone: {persona['tone']}.
    Constraints: {persona['constraints']}.
    User says: {user_message}
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # You can change this to another model
            messages=[{"role": "system", "content": prompt}],
            max_tokens=250
        )
        reply = response.choices[0].message["content"].strip()
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
