import os

from flask import Flask, request, jsonify
from flask_cors import CORS
from google import genai

app = Flask(__name__)
CORS(app)

client = genai.Client(
    api_key=os.environ.get("GEMINI_API_KEY")
)


@app.route("/")
def home():
    return "JARVIS ONLINE"


@app.route("/teste", methods=["GET"])
def teste():
    return jsonify({
        "status": "ok",
        "message": "O cérebro do Jarvis está acessível."
    })


@app.route("/jarvis", methods=["POST"])
def jarvis():

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Nenhum dado recebido"
        }), 400

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

Usuário:
{mensagem}
"""

    try:

        resposta = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return jsonify({
            "response": resposta.text
        })

    except Exception as erro:

        print("ERRO GEMINI:", erro)

        return jsonify({
            "error": "Erro ao consultar a inteligência artificial."
        }), 500


if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000))
    )
