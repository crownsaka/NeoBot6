from flask import Flask, request, jsonify
import requests
from dotenv import load_dotenv
import os
from flask_cors import CORS
import markdown

# Load environment variables
load_dotenv()

# Flask app setup
app = Flask(__name__)
CORS(app)

# Constants
AI_NAME = "NeoBot"
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL = "mistralai/mistral-small-3.2-24b-instruct:free"

# Chat history (in-memory)
chat_history = []

# Core function to get response from OpenRouter
def get_ai_response(prompt):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:25000",
        "X-Title": "NeoBotAI",
    }
    data = {
        "model": MODEL,
        "messages": [
            {
                "role": "system",
                "content": "You are a smart and helpful assistant named NeoBot."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    }

    try:
        response = requests.post(OPENROUTER_API_URL, headers=headers, json=data)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"API Error: {e}")
        return "Sorry, I encountered an error processing your request."

# Main API route
@app.route("/api/ask", methods=["POST"])
def ask():
    try:
        data = request.get_json()
        user_input = data.get("user_input")

        if not user_input:
            return jsonify({"error": "Missing 'user_input'"}), 400

        ai_response = get_ai_response(user_input)
        formatted_response = markdown.markdown(ai_response)

        # Append to chat history
        chat_history.append({"sender": "user", "message": user_input})
        chat_history.append({"sender": AI_NAME, "message": formatted_response})

        return jsonify({
            "status": "success",
            "response": formatted_response,
            "history": chat_history
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Health check route
@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "status": "running",
        "message": "Send POST requests to /api/ask with 'user_input'"
    })

# Run the app
if __name__ == "__main__":
    app.run(port=25000, debug=True)
