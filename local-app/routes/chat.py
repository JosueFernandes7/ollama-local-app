from flask_smorest import Blueprint
from flask import jsonify
from schemas.schemas import ChatRequestSchema
from models.model_service import chat as model_chat, model_exists

chat_bp = Blueprint(
    "chat",
    __name__,
    url_prefix="/chat",
    description="Operações de interação com os modelos de linguagem"
)

@chat_bp.route("/", methods=["POST"])
@chat_bp.arguments(ChatRequestSchema, location="json")
@chat_bp.doc(
    summary="Envia mensagens para um modelo",
    description="Permite enviar mensagens para um modelo disponível e receber uma resposta.",
    responses={
        200: {
            "description": "Resposta do modelo",
            "content": {
                "application/json": {
                    "example": {
                        "response": "A capital do Brasil é Brasília."
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
        404: {
            "description": "Modelo não encontrado",
            "content": {
                "application/json": {
                    "example": {
                        "error": "O modelo 'llama3.1:8b' não está disponível."
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
def chat(data):
    """Envia mensagens para um modelo disponível."""
    model_name = data["model"]
    messages = data["messages"]
    options = data.get("options", {})

    if not model_exists(model_name):
        return jsonify({"error": f"O modelo '{model_name}' não está disponível."}), 404

    try:
        response = model_chat(model_name, messages, options)
        return jsonify({"response": response['message']['content']}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
