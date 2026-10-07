import os
from flask import Flask, request, jsonify
from google import genai
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

client = genai.Client(
    api_key=os.environ.get("GEMINI_API_KEY")
)

@app.route("/")
def home():
    return "JARVIS ONLINE"

@app.route("/jarvis", methods=["POST"])
def jarvis():

    data = request.get_json()

    mensagem = data.get("message", "")

    if not mensagem:
        return jsonify({
            "error": "Mensagem vazia"
        }), 400

    prompt = f"""
Você é JARVIS, um assistente pessoal de inteligência artificial.

Personalidade:
- inteligente
- educado
- objetivo
- natural
- prestativo
- responde sempre em português do Brasil

Você deve conversar naturalmente com o usuário.

Usuário:
{mensagem}
"""

    resposta = client.models.generate_content(
        model="gemini-3.8-flash",
        contents=prompt
    )

    return jsonify({
        "response": resposta.text
    })


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000))
    )
