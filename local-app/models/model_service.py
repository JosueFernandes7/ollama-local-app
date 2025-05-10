from concurrent.futures import ThreadPoolExecutor
import ollama
from core.config import settings

client = ollama.Client(host=settings.OLLAMA_HOST)
executor = ThreadPoolExecutor(max_workers=settings.MAX_WORKERS)

def model_exists(model_name):
    """Verifica se o modelo existe."""
    models = [m.model for m in client.list().models]
    return model_name in models

def download_model(model_name):
    """Baixa o modelo de forma assíncrona."""
    client.pull(model_name)

def delete_model(model_name):
    """Remove o modelo do servidor."""
    client.delete(model_name)

def list_models():
    """Retorna todos os modelos disponíveis."""
    return [m.model for m in client.list().models]

def chat(model, messages, options=None):
    """Realiza a interação com o modelo."""
    return client.chat(model=model, messages=messages, options=options or {})
