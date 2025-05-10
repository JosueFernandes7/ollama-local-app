# app.py
from flask import Flask, jsonify, request
from core.config import settings
from concurrent.futures import ThreadPoolExecutor
import ollama

app = Flask(__name__)
app.config.from_object(settings)

client = ollama.Client(
    host=settings.OLLAMA_HOST
)
executor = ThreadPoolExecutor(max_workers=4)

def model_exists(model):
    """
    Verifica se o modelo existe
    """
    try:
        models = [m.model for m in client.list().models]
        if model in models:
            return True
        else:
            return False
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def download_model(model):
    try:
        client.pull(model)
        print(f"Modelo '{model}' baixado com sucesso!")
    except Exception as e:
        print(f"Erro ao baixar o modelo '{model}': {e}")
        
# OK
@app.route("/healthcheck", methods=["GET"])
def healthcheck():
    return jsonify({"message": "OK"}), 200

# OK
@app.route("/list", methods=["GET"])
def list_models():
    try:
        # Extrai apenas os nomes dos modelos corretamente
        models = [m.model for m in client.list().models]

        return jsonify(models), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
# Ok
@app.route("/create", methods=["POST"])
def create_model():
    data = request.json
    model = data.get("model", None)
    
    if not model:
        return jsonify({"error": "O campo 'model' é obrigatório"}), 400
    
    if model_exists(model):
        return jsonify({"message": f"O modelo '{model}' já está disponível."}), 200
    
    # Download de forma assíncrona
    try:
        
        # Baixando o modelo
        executor.submit(download_model, model)
        return jsonify({"message": f"O modelo '{model}' está sendo baixado."}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# OK
@app.route("/delete/<model>", methods=["DELETE"])
def delete_chat(model):
    try:
        if not model_exists(model):
            return jsonify({"message": f"O modelo '{model}' não está disponível."}), 404

        client.delete(model)
        
        return jsonify({"message": f"O modelo '{model}' foi removido."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    model = data.get("model")
    messages = data.get("messages")
    temperature = data.get("temperature", 0.7)
    top_p = data.get("top_p", 0.9)
    top_k = data.get("top_k", 40)
    repeat_penalty = data.get("repeat_penalty", 1.0)

    if not model:
        return jsonify({"error": "O campo 'model' é obrigatório"}), 400

    if not model_exists(model):
        return jsonify({"error": f"O modelo '{model}' não está disponível"}), 404

    if not messages or not isinstance(messages, list):
        return jsonify({"error": "O campo 'messages' é obrigatório e deve ser uma lista"}), 400

    try:
        response = client.chat(
            model=model,
            messages=messages,
            options={
                "temperature": temperature,
                "top_p": top_p,
                "top_k": top_k,
                "repeat_penalty": repeat_penalty
            }
        )
        return jsonify({"response": response['message']['content']}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(port=5000, debug=True)
