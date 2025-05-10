from flask_smorest import Blueprint
from flask import jsonify

healthcheck_bp = Blueprint(
    "healthcheck",
    __name__,
    url_prefix="/healthcheck",
    description="Operações de verificação de saúde do servidor"
)

@healthcheck_bp.route("/", methods=["GET"])
@healthcheck_bp.doc(
    summary="Verifica o status do servidor",
    description="Endpoint simples para verificar se o servidor está ativo e respondendo.",
    responses={
        200: {
            "description": "Servidor ativo",
            "content": {
                "application/json": {
                    "example": {
                        "message": "OK"
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
def healthcheck():
    """Verifica se o servidor está ativo."""
    return jsonify({"message": "OK"}), 200
