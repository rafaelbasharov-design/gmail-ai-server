import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import openai

# Создаем Flask-приложение
app = Flask(__name__)
CORS(app)

# Ключ берем из Environment Variables в Render
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/")
def home():
    return jsonify({"message": "✅ Gmail AI Server is running!"})

@app.route("/generate-reply", methods=["POST"])
def generate_reply():
    try:
        data = request.json
        user_message = data.get("message", "")

        if not user_message:
            return jsonify({"error": "No message provided"}), 400

        # Запрос в OpenAI
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Ты помощник для Gmail, создающий вежливые ответы на письма."},
                {"role": "user", "content": user_message}
            ],
            max_tokens=200
        )

        ai_reply = response.choices[0].message.content.strip()
        return jsonify({"reply": ai_reply})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
