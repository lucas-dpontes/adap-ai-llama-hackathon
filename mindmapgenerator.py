from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any
from groq import Groq
import json

app = FastAPI()

class MindMapGenerator:
    """
    Classe para gerar um mapa mental com base em um assunto fornecido,
    utilizando a API do Grog para obter os dados do mapa.
    """

    def __init__(self, api_key: str):
        """
        Inicializa a instância da classe MindMapGenerator.

        Parâmetros:
            api_key (str): A chave de API para autenticação no Grog.
        """
        self.client = Groq(api_key=api_key)

    def create_agent(self, role_name: str, initial_message: str) -> str:
        """
        Cria um agente no Grog e obtém a resposta completa para uma mensagem inicial.

        Parâmetros:
            role_name (str): O nome do papel do agente para o contexto da mensagem.
            initial_message (str): A mensagem inicial enviada ao agente.

        Retorna:
            str: A resposta completa do agente em formato de string.
        """
        completion = self.client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": initial_message}],
            temperature=0.5,
            max_tokens=1512,
            top_p=1,
            stream=True,
            stop=None,
        )
        response = ""
        for chunk in completion:
            content = chunk.choices[0].delta.content
            if content:
                response += content
        return response

    def generate_mind_map(self, subject: str) -> Optional[Dict[str, Any]]:
        """
        Gera um mapa mental para o assunto fornecido.

        Parâmetros:
            subject (str): O assunto para o qual o mapa mental será gerado.

        Retorna:
            dict: Dicionário representando o mapa mental em formato JSON.
                  Retorna None se não for possível gerar um JSON válido.
        """
        message = (
            f"Create a mind map for the subject '{subject}' in the following JSON format. "
            "It should include nodes and edges. Each node should have fields 'id', 'label', 'type', and 'parent'. "
            "The 'type' should be 'general_subject' for the main topic, 'category' for high-level branches, "
            "and 'sub_category' for subtopics under each category. Each edge should connect a source node to a target node.\n"
            "Example format:\n\n"
            "{\n"
            "  \"general_subject\": \"{subject}\",\n"
            "  \"nodes\": [\n"
            "    {\"id\": \"1\", \"label\": \"{subject}\", \"type\": \"general_subject\"},\n"
            "    {\"id\": \"2\", \"label\": \"Category 1\", \"type\": \"category\", \"parent\": \"1\"},\n"
            "    {\"id\": \"3\", \"label\": \"Subcategory 1\", \"type\": \"sub_category\", \"parent\": \"2\"}\n"
            "  ],\n"
            "  \"edges\": [\n"
            "    {\"source\": \"1\", \"target\": \"2\"},\n"
            "    {\"source\": \"2\", \"target\": \"3\"}\n"
            "  ]\n"
            "}\n"
            "Please use this format and only output valid JSON. Don't write anything after"
        )

        # Gera a resposta do agente para o mapa mental
        response = self.create_agent("Mind Map Generator", message.replace("{subject}", subject))

        # Converte a resposta para JSON
        try:
            mind_map_data = json.loads(response)
            return mind_map_data
        except json.JSONDecodeError:
            print("Erro: A resposta da IA não está em formato JSON válido.")
            return None

# Classe de entrada para a requisição
class MindMapRequest(BaseModel):
    subject: str

# Configuração da chave da API do Grog
API_KEY = "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"
mind_map_generator = MindMapGenerator(api_key=API_KEY)

@app.post("/generate-mind-map")
async def generate_mind_map(request: MindMapRequest):
    """
    Gera um mapa mental com base em um assunto fornecido.

    Parâmetros:
        request (MindMapRequest): O assunto desejado para a geração do mapa mental.

    Retorna:
        dict: O mapa mental gerado em formato JSON.
    """
    result = mind_map_generator.generate_mind_map(request.subject)
    if not result:
        raise HTTPException(status_code=400, detail="Não foi possível gerar o mapa mental.")
    return result
