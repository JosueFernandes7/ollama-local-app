import os

class Settings:
    OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11400")
    API_TITLE = "Ollama API"
    API_VERSION = "1.0.0"
    OPENAPI_VERSION = "3.0.3"
    OPENAPI_URL_PREFIX = "/docs"
    OPENAPI_SWAGGER_UI_PATH = "/swagger"
    OPENAPI_SWAGGER_UI_URL = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    MAX_WORKERS = int(os.getenv("MAX_WORKERS", 4))

settings = Settings()
