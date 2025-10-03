# app.py
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI

app = Flask(__name__)
CORS(app)

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

@app.route("/")
def home():
    return jsonify({"message": "Gmail AI Server running with new OpenAI SDK"})

@app.route("/generate-reply", methods=["POST"])
def generate_reply():
    try:
        data = request.get_json(force=True)
        text = data.get("message", "")
        if not text or len(text.strip()) < 3:
            return jsonify({"error": "No message provided"}), 400

        # Новый синтаксис для openai>=1.0.0
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an assistant that writes short polite email replies."},
                {"role": "user", "content": f"Reply to this email:\n\n{text}"}
            ],
            max_tokens=250,
            temperature=0.6
        )

        reply = response.choices[0].message.content.strip()
        return jsonify({"reply": reply})
    except Exception as e:
        app.logger.exception("generate-reply error")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
