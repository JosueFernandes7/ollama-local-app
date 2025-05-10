from flask import Blueprint, jsonify, request
from models.model_service import chat as model_chat, model_exists

chat_bp = Blueprint("chat", __name__)

@chat_bp.route("/chat", methods=["POST"])
def chat():
    data = request.json
    model_name = data.get("model")
    messages = data.get("messages")
    options = data.get("options", {})

    if not model_name:
        return jsonify({"error": "O campo 'model' é obrigatório"}), 400

    if not model_exists(model_name):
        return jsonify({"error": f"O modelo '{model_name}' não está disponível."}), 404

    if not messages or not isinstance(messages, list):
        return jsonify({"error": "O campo 'messages' é obrigatório e deve ser uma lista"}), 400

    try:
        response = model_chat(model_name, messages, options)
        return jsonify({"response": response['message']['content']}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
