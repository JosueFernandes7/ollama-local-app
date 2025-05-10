import ollama
from core.config import settings
from core.logger import logger

client = ollama.Client(host=settings.OLLAMA_HOST)

def model_exists(model_name):
    """Verifica se o modelo existe."""
    try:
        return model_name in list_models()
    except Exception as e:
        logger.error(f"Erro ao verificar existência do modelo '{model_name}': {e}")
        return False

def download_model(model_name):
    """Baixa o modelo de forma assíncrona."""
    try:
        logger.info(f"Iniciando download do modelo '{model_name}'...")
        client.pull(model_name)
        logger.info(f"Modelo '{model_name}' baixado com sucesso.")
    except Exception as e:
        logger.error(f"Erro ao baixar o modelo '{model_name}': {e}")

def delete_model(model_name):
    """Remove o modelo do servidor."""
    try:
        logger.info(f"Removendo modelo '{model_name}'...")
        client.delete(model_name)
        logger.info(f"Modelo '{model_name}' removido com sucesso.")
    except Exception as e:
        logger.error(f"Erro ao remover o modelo '{model_name}': {e}")

def list_models():
    """Retorna todos os modelos disponíveis."""
    try:
        models = [m.model for m in client.list().models]
        logger.debug(f"Modelos disponíveis: {models}")
        return models
    except Exception as e:
        logger.error(f"Erro ao listar modelos: {e}")
        return []

def chat(model, messages, options=None):
    """Realiza a interação com o modelo."""
    try:
        logger.info(f"Iniciando chat com o modelo '{model}'...")
        response = client.chat(model=model, messages=messages, options=options or {})
        content = response.get("message", {}).get("content", "")
        logger.debug(f"Resposta do modelo '{model}': {content}")
        return response
    except Exception as e:
        logger.error(f"Erro no chat com o modelo '{model}': {e}")
        raise e
