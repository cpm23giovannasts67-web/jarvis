import os

from flask import Flask, request, jsonify
from flask_cors import CORS
from google import genai

app = Flask(__name__)

CORS(app)

# Conecta ao Gemini usando a variável de ambiente do Render
client = genai.Client(
    api_key=os.environ.get("GEMINI_API_KEY")
)


# =========================
# TESTE DO SERVIDOR
# =========================

@app.route("/")
def home():

    return "JARVIS ONLINE"


# =========================
# TESTE DO GEMINI
# =========================

@app.route("/teste", methods=["GET"])
def teste():

    try:

        resposta = client.models.generate_content(
            model="gemini-2.5-flash",
            contents="Responda apenas: JARVIS, cérebro funcionando."
        )

        return jsonify({
            "status": "ok",
            "gemini": resposta.text
        })

    except Exception as erro:

        print("ERRO GEMINI:", erro)

        return jsonify({
            "status": "erro",
            "erro": str(erro)
        }), 500


# =========================
# CÉREBRO PRINCIPAL
# =========================

@app.route("/jarvis", methods=["POST"])
def jarvis():

    try:

        data = request.get_json()

        if not data:

            return jsonify({
                "error": "Nenhum dado recebido."
            }), 400


        mensagem = data.get("message", "")


        if not mensagem:

            return jsonify({
                "error": "Mensagem vazia."
            }), 400


        prompt = f"""
Você é JARVIS, um assistente pessoal de inteligência artificial.

PERSONALIDADE:

- Inteligente
- Educado
- Natural
- Prestativo
- Objetivo
- Responde em português do Brasil
- Pode conversar naturalmente com o usuário
- Não diga que é apenas um chatbot
- Quando não souber algo, seja honesto

O usuário está conversando diretamente com você.

Mensagem do usuário:

{mensagem}

Responda de maneira natural e útil.
"""


        resposta = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )


        return jsonify({
            "response": resposta.text
        })


    except Exception as erro:

        print("ERRO NO JARVIS:", erro)

        return jsonify({
            "error": "Erro ao processar a mensagem.",
            "details": str(erro)
        }), 500


# =========================
# INICIALIZAÇÃO
# =========================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000))
    )
