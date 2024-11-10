from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Union
from groq import Groq
import random
import json

app = FastAPI()

class WordSearchGenerator:
    def __init__(self, api_key):
        self.client = Groq(api_key=api_key)

    def create_agent(self, role_name, initial_message):
        completion = self.client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": initial_message}],
            temperature=0.5,
            max_tokens=512,
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

    def get_words_from_agent(self, topic, max_attempts=3):
        for attempt in range(max_attempts):
            message = (
                f"Retorne exatamente 10 palavras curtas relacionadas ao tópico '{topic}', "
                "no formato JSON e sem nenhum texto adicional. A resposta deve estar neste formato:\n"
                "[\"palavra1\", \"palavra2\", \"palavra3\", ...]"
            )
            response = self.create_agent("Word Generator", message)
            try:
                words = json.loads(response)
                if isinstance(words, list) and len(words) == 10 and all(isinstance(word, str) for word in words):
                    return [word.strip().upper() for word in words]
            except json.JSONDecodeError:
                continue
        return []

    def place_word_in_grid(self, grid, word):
        max_rows, max_cols = len(grid), len(grid[0])
        word_len = len(word)
        for _ in range(100):
            start_row = random.randint(0, max_rows - 1)
            start_col = random.randint(0, max_cols - 1)
            direction = random.choice([(0, 1), (1, 0), (1, 1)])
            end_row = start_row + (word_len - 1) * direction[0]
            end_col = start_col + (word_len - 1) * direction[1]
            if 0 <= end_row < max_rows and 0 <= end_col < max_cols:
                if all(grid[start_row + i * direction[0]][start_col + i * direction[1]] in ("", word[i]) for i in range(word_len)):
                    for i in range(word_len):
                        grid[start_row + i * direction[0]][start_col + i * direction[1]] = word[i]
                    return {
                        "word": word,
                        "start": [start_row, start_col],
                        "end": [end_row, end_col]
                    }
        return None

    def generate_word_search(self, topic):
        words = self.get_words_from_agent(topic)
        if not words:
            return None
        grid = [["" for _ in range(10)] for _ in range(10)]
        answers = []
        for word in words:
            result = self.place_word_in_grid(grid, word)
            if result:
                answers.append(result)
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        for row in range(10):
            for col in range(10):
                if grid[row][col] == "":
                    grid[row][col] = random.choice(alphabet)
        return {
            "grid": grid,
            "answers": answers
        }

# Classe de entrada para a requisição
class WordSearchRequest(BaseModel):
    topic: str

# Configuração da chave da API do Grog
API_KEY = "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"
word_search_generator = WordSearchGenerator(api_key=API_KEY)

@app.post("/generate-word-search")
async def generate_word_search(request: WordSearchRequest):
    """
    Gera um caça-palavras com base em um tópico fornecido.

    Parâmetros:
        request (WordSearchRequest): O tópico desejado para a geração do caça-palavras.

    Retorna:
        dict: A grade do caça-palavras e a lista de palavras e suas coordenadas.
    """
    result = word_search_generator.generate_word_search(request.topic)
    if not result:
        raise HTTPException(status_code=400, detail="Não foi possível gerar o caça-palavras.")
    return result

