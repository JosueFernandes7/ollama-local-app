from flask_smorest import Blueprint
from flask import jsonify, request
from models.model_service import model_exists, download_model, delete_model, list_models
from concurrent.futures import ThreadPoolExecutor
from core.config import settings
from schemas.schemas import ModelSchema
model_bp = Blueprint(
    "models",
    __name__,
    url_prefix="/models",
    description="Operações relacionadas ao gerenciamento de modelos"
)

executor = ThreadPoolExecutor(max_workers=settings.MAX_WORKERS)

@model_bp.route("/", methods=["GET"])
@model_bp.doc(
    summary="Lista todos os modelos disponíveis",
    description="Retorna uma lista com os nomes dos modelos atualmente disponíveis no servidor.",
    responses={
        200: {
            "description": "Lista de modelos disponíveis",
            "content": {
                "application/json": {
                    "example": ["llama3.1:8b", "qwen3:0.6b"]
                }
            }
        },
        500: {
            "description": "Erro interno do servidor",
            "content": {
                "application/json": {
                    "example": {
                        "error": "Descrição do erro"
                    }
                }
            }
        }
    }
)
def list_available_models():
    try:
        models = list_models()
        return jsonify(models), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@model_bp.route("/", methods=["POST"])
@model_bp.arguments(ModelSchema, location="json")
@model_bp.doc(
    summary="Cria um novo modelo no servidor",
    description="Inicia o download de um novo modelo e o disponibiliza no servidor.",
    responses={
        201: {
            "description": "Modelo criado com sucesso",
            "content": {
                "application/json": {
                    "example": {
                        "message": "O modelo 'llama3.1:8b' está sendo baixado."
                    }
                }
            }
        },
        400: {
            "description": "Requisição inválida",
            "content": {
                "application/json": {
                    "example": {
                        "error": "O campo 'model' é obrigatório"
                    }
                }
            }
        },
        500: {
            "description": "Erro interno do servidor",
            "content": {
                "application/json": {
                    "example": {
                        "error": "Descrição do erro"
                    }
                }
            }
        }
    }
)
def create_model(data):
    model_name = data["model"]

    if not model_name:
        return jsonify({"error": "O campo 'model' é obrigatório"}), 400

    if model_exists(model_name):
        return jsonify({"message": f"O modelo '{model_name}' já está disponível."}), 200

    try:
        executor.submit(download_model, model_name)
        return jsonify({"message": f"O modelo '{model_name}' está sendo baixado."}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@model_bp.route("/<model_name>", methods=["DELETE"])
@model_bp.doc(
    summary="Remove um modelo do servidor",
    description="Remove permanentemente um modelo do servidor.",
    parameters=[
        {
            "name": "model_name",
            "in": "path",
            "description": "Nome do modelo a ser removido",
            "required": True,
            "example": "llama3.1:8b"
        }
    ],
    responses={
        200: {
            "description": "Modelo removido com sucesso",
            "content": {
                "application/json": {
                    "example": {
                        "message": "O modelo 'llama3.1:8b' foi removido."
                    }
                }
            }
        },
        404: {
            "description": "Modelo não encontrado",
            "content": {
                "application/json": {
                    "example": {
                        "message": "O modelo 'llama3.1:8b' não está disponível."
                    }
                }
            }
        },
        500: {
            "description": "Erro interno do servidor",
            "content": {
                "application/json": {
                    "example": {
                        "error": "Descrição do erro"
                    }
                }
            }
        }
    }
)
def remove_model(model_name):
    try:
        if not model_exists(model_name):
            return jsonify({"message": f"O modelo '{model_name}' não está disponível."}), 404

        delete_model(model_name)
        return jsonify({"message": f"O modelo '{model_name}' foi removido."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
