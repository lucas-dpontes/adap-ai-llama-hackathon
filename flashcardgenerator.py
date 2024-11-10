from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any
from groq import Groq
import json
import re

app = FastAPI()

class FlashcardGenerator:
    """
    Classe para gerar flashcards personalizados para um assunto fornecido,
    utilizando a API do Grog para obter os dados dos flashcards.
    """

    def __init__(self, api_key: str):
        self.client = Groq(api_key=api_key)

    def clean_response(self, response: str) -> str:
        """
        Limpa a resposta da IA corrigindo problemas comuns, como aspas duplicadas no campo "id".

        Parâmetros:
            response (str): A resposta em formato de string JSON gerada pela IA.

        Retorna:
            str: A resposta limpa e pronta para decodificação JSON.
        """
        response = re.sub(r'"id": (\d+)",', r'"id": \1,', response)
        return response

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
            max_tokens=2000,
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

    def create_flashcards(self, subject: str, num_flashcards: int = 5) -> Optional[Dict[str, Any]]:
        """
        Gera flashcards para o assunto fornecido em formato JSON.

        Parâmetros:
            subject (str): O assunto para o qual os flashcards serão gerados.
            num_flashcards (int): Número de flashcards desejados.

        Retorna:
            dict: Dicionário representando os flashcards em formato JSON.
                  Retorna None se não for possível gerar um JSON válido.
        """
        message = (
            f"Crie {num_flashcards} flashcards para o assunto '{subject}' no formato JSON, sem introduções ou explicações adicionais. "
            "A resposta deve estar neste exato formato, com uma lista de flashcards, cada um contendo: 'id' (número sem aspas), 'front', 'back', 'category', "
            "'difficulty', 'tags', e 'image'. O JSON deve começar diretamente sem qualquer introdução:\n\n"
            "{\n"
            f"  \"general_subject\": \"{subject}\",\n"
            "  \"flashcards\": [\n"
            "    {\n"
            "      \"id\": 1,\n"
            "      \"front\": \"Pergunta do flashcard\",\n"
            "      \"back\": \"Resposta do flashcard\",\n"
            "      \"category\": \"Categoria\",\n"
            "      \"difficulty\": \"Nível de dificuldade\",\n"
            "      \"tags\": [\"tag1\", \"tag2\"],\n"
            "      \"image\": \"[Inserir URL de uma imagem relevante aqui]\"\n"
            "    },\n"
            "    {...}\n"
            "  ]\n"
            "}"
        )

        response = self.create_agent("Flashcard Generator", message.replace("{subject}", subject))

        print("Resposta da IA:", response)

        try:
            response = self.clean_response(response)

            if '"general_subject"' not in response:
                response = f'{{"general_subject": "{subject}", "flashcards": {response}}}'

            flashcard_data = json.loads(response)
            return flashcard_data
        except json.JSONDecodeError as e:
            print("Erro ao decodificar JSON:", e)
            return None

# Classe de entrada para a requisição
class FlashcardRequest(BaseModel):
    subject: str
    num_flashcards: int = 5

# Configuração da chave da API do Grog
API_KEY = "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"
flashcard_generator = FlashcardGenerator(api_key=API_KEY)

@app.post("/generate-flashcards")
async def generate_flashcards(request: FlashcardRequest):
    """
    Gera flashcards personalizados com base em um assunto e o número desejado de flashcards.

    Parâmetros:
        request (FlashcardRequest): O assunto e o número de flashcards desejados.

    Retorna:
        dict: Os flashcards gerados em formato JSON.
    """
    result = flashcard_generator.create_flashcards(request.subject, request.num_flashcards)
    if not result:
        raise HTTPException(status_code=400, detail="Não foi possível gerar os flashcards.")
    return result
