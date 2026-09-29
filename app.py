import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from google import genai
from chatbot_config import SYSTEM_PROMPT

load_dotenv()
app = Flask(__name__)

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError("GEMINI_API_KEY is missing. Add it to your .env file.")

client = genai.Client(api_key=api_key)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    user_message = (data.get("message") or "").strip()
    if not user_message:
        return jsonify({"error": "Please enter your agriculture question."}), 400

    prompt = f"{SYSTEM_PROMPT}\n\nFarmer/User: {user_message}\nAssistant:"

    try:
        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=prompt
        )
        return jsonify({"reply": response.text or "Sorry, I could not generate an answer."})
    except Exception as e:
        return jsonify({"error": f"Gemini API error: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
