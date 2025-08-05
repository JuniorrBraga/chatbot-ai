# Arquivo: app.py
# Responsabilidade: Ponto de entrada da aplicação, gerencia as rotas web e orquestra os serviços.

from flask import Flask, request, jsonify
from services.ghl_client import GHLClient
from services.gemini_client import GeminiClient
import json

app = Flask(__name__)

# Inicializa os nossos clientes de serviço
ghl_service = GHLClient()
gemini_service = GeminiClient()

@app.route('/webhook/ghl', methods=['POST'])
def ghl_webhook_handler():
    """
    Recebe a notificação (webhook) do GHL sempre que um novo lead manda mensagem.
    """
    data = request.json
    print(">>> Webhook Recebido do GHL:")
    print(json.dumps(data, indent=2))

    contact_id = data.get('contactId')
    user_message = data.get('body')

    if not contact_id or not user_message:
        print("!!! Erro: Faltando contact_id ou mensagem no corpo do webhook.")
        return jsonify({"status": "error", "message": "Faltando contact_id ou mensagem"}), 400

    # Em um projeto futuro, aqui você buscaria o histórico da conversa de um banco de dados.
    # Por enquanto, mantemos um histórico vazio para cada nova mensagem.
    conversation_history = [] 

    # Obter a classificação e a resposta da IA usando o serviço do Gemini
    classification, reply_message = gemini_service.get_ai_classification_and_reply(
        user_message=user_message,
        conversation_history=conversation_history
    )

    print(f">>> Decisão da IA: Classificação='{classification}', Resposta='{reply_message}'")

    # Enviar a resposta da IA para o lead através do serviço do GHL
    if reply_message:
        ghl_service.send_message(contact_id, reply_message)

    # Se a IA classificou o lead, adicione a tag correspondente no GHL
    if classification and classification != "continuar_conversa":
        ghl_service.add_tag(contact_id, classification)

    return jsonify({"status": "success"}), 200

if __name__ == '__main__':
    # Para rodar em produção, use um servidor WSGI como Gunicorn.
    # Ex: gunicorn --bind 0.0.0.0:5000 app:app
    app.run(host='0.0.0.0', port=5000, debug=True)