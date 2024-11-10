from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
from groq import Groq

app = FastAPI()

class EducationalAssistant:
    """
    Classe para criar uma interação de assistente educacional com a API Groq.
    Permite ao usuário enviar mensagens em texto e receber respostas interativas.
    """

    def __init__(self, api_key: str, model: str = "llama3-8b-8192"):
        """
        Inicializa a instância da classe EducationalAssistant.
        
        Parâmetros:
            api_key (str): Chave de API para autenticação no Groq.
            model (str): O modelo usado para gerar respostas (padrão: llama3-8b-8192).
        """
        self.client = Groq(api_key=api_key)
        self.model = model
        self.conversation_history: List[Dict[str, str]] = []

    def send_message(self, user_message: str, temperature: float = 1.0, max_tokens: int = 1024) -> str:
        """
        Envia uma mensagem do usuário para a API e retorna a resposta.
        
        Parâmetros:
            user_message (str): Mensagem enviada pelo usuário.
            temperature (float): Controle da criatividade da resposta (0 a 1).
            max_tokens (int): Número máximo de tokens na resposta.
        
        Retorna:
            str: A resposta gerada pelo assistente.
        """
        # Adiciona a mensagem do usuário ao histórico de conversação
        self.conversation_history.append({"role": "user", "content": user_message})

        # Cria a solicitação de conclusão com o histórico de conversação
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=self.conversation_history,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=1,
            stream=True,
            stop=None,
        )

        # Armazena a resposta e adiciona ao histórico
        assistant_response = ""
        for chunk in completion:
            content = chunk.choices[0].delta.content
            if content:
                assistant_response += content

        # Adiciona a resposta ao histórico de conversação
        self.conversation_history.append({"role": "assistant", "content": assistant_response})

        return assistant_response

    def clear_history(self):
        """
        Limpa o histórico de conversação.
        """
        self.conversation_history = []

# Configuração da chave da API do Groq
API_KEY = "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"
assistant = EducationalAssistant(api_key=API_KEY)

# Classe de entrada para a requisição
class MessageRequest(BaseModel):
    message: str
    temperature: Optional[float] = 1.0
    max_tokens: Optional[int] = 1024

# Endpoint para enviar mensagens e receber respostas
@app.post("/send-message")
async def send_message(request: MessageRequest):
    """
    Envia uma mensagem do usuário para o assistente educacional e recebe uma resposta.
    
    Parâmetros:
        request (MessageRequest): A mensagem enviada pelo usuário, temperatura e max_tokens.
        
    Retorna:
        str: A resposta gerada pelo assistente.
    """
    response = assistant.send_message(
        user_message=request.message,
        temperature=request.temperature,
        max_tokens=request.max_tokens
    )
    if not response:
        raise HTTPException(status_code=500, detail="Erro ao gerar resposta do assistente.")
    return {"response": response}

# Endpoint para limpar o histórico de conversação
@app.post("/clear-history")
async def clear_history():
    """
    Limpa o histórico de conversação do assistente educacional.
    """
    assistant.clear_history()
    return {"message": "Histórico de conversação limpo com sucesso."}
