from flask import Blueprint, jsonify, request
from models.model_service import model_exists, download_model, delete_model, list_models
from concurrent.futures import ThreadPoolExecutor
from core.config import settings

model_bp = Blueprint("model", __name__)

executor = ThreadPoolExecutor(max_workers=settings.MAX_WORKERS)

@model_bp.route("/models", methods=["GET"])
def list_available_models():
    try:
        models = list_models()
        return jsonify(models), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@model_bp.route("/models", methods=["POST"])
def create_model():
    data = request.json
    model_name = data.get("model")

    if not model_name:
        return jsonify({"error": "O campo 'model' é obrigatório"}), 400

    if model_exists(model_name):
        return jsonify({"message": f"O modelo '{model_name}' já está disponível."}), 200

    try:
        executor.submit(download_model, model_name)
        return jsonify({"message": f"O modelo '{model_name}' está sendo baixado."}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@model_bp.route("/models/<model_name>", methods=["DELETE"])
def remove_model(model_name):
    try:
        if not model_exists(model_name):
            return jsonify({"message": f"O modelo '{model_name}' não está disponível."}), 404

        delete_model(model_name)
        return jsonify({"message": f"O modelo '{model_name}' foi removido."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
