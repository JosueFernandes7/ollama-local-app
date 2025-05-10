from flask import Flask
from flask_smorest import Api
from core.config import settings
from routes.healthcheck import healthcheck_bp
from routes.model import model_bp
from routes.chat import chat_bp
from core.logger import logger

app = Flask(__name__)

# Configuração do Flask-Smorest
app.config.update(settings.FLASK_CONFIG)

api = Api(app)

# Registro dos Blueprints
api.register_blueprint(healthcheck_bp)
api.register_blueprint(model_bp)
api.register_blueprint(chat_bp)

logger.info("Iniciando a API do Ollama...")

if __name__ == "__main__":
    app.run(port=5000, debug=True)
