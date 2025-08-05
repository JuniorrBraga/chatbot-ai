# Arquivo: services/ghl_client.py
# Responsabilidade: Lidar com todas as interações com a API do GoHighLevel.

import requests
import os
from dotenv import load_dotenv

load_dotenv() # Carrega as variáveis do arquivo .env

class GHLClient:
    def __init__(self):
        self.api_key = os.getenv("GHL_API_KEY")
        if not self.api_key:
            raise ValueError("A chave de API do GHL (GHL_API_KEY) não foi encontrada no arquivo .env")
        
        self.base_url = "https://services.leadconnectorhq.com"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Version": "2021-07-28",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

    def send_message(self, contact_id, message_text):
        """Envia uma mensagem para um contato."""
        url = f"{self.base_url}/conversations/messages"
        payload = {
            "type": "SMS",  # ou 'Email', etc.
            "contactId": contact_id,
            "message": message_text
        }
        
        try:
            response = requests.post(url, headers=self.headers, json=payload)
            response.raise_for_status() # Lança um erro para respostas 4xx/5xx
            print(f"GHL: Mensagem enviada para {contact_id} com sucesso. Status: {response.status_code}")
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"!!! GHL Erro ao enviar mensagem: {e}")
            return None

    def add_tag(self, contact_id, tag):
        """Adiciona uma tag a um contato."""
        # A API de tags usa uma versão diferente
        tag_headers = self.headers.copy()
        tag_headers["Version"] = "2021-04-15"
        
        url = f"{self.base_url}/contacts/{contact_id}/tags"
        payload = {'tags': [tag]}

        try:
            response = requests.post(url, headers=tag_headers, json=payload)
            response.raise_for_status()
            print(f"GHL: Tag '{tag}' adicionada para {contact_id} com sucesso. Status: {response.status_code}")
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"!!! GHL Erro ao adicionar tag: {e}")
            return None