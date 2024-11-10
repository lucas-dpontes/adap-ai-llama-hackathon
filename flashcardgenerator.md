# Flashcard Generator API

## Descrição

O `flashcardgenerator.py` é um módulo que utiliza a API do Groq para gerar flashcards personalizados sobre um determinado assunto. A API permite especificar o tema e o número de flashcards a serem gerados, retornando cada flashcard com informações detalhadas.

## Estrutura do Código

### Classe `FlashcardGenerator`

- **Descrição**: Gera flashcards personalizados com base em um tema.
- **Métodos**:
  - `__init__(api_key: str)`: Inicializa a classe com a chave de API do Groq.
  - `clean_response(response: str) -> str`: Limpa e corrige a resposta JSON.
  - `create_agent(role_name: str, initial_message: str) -> str`: Cria um agente Groq e obtém uma resposta completa.
  - `create_flashcards(subject: str, num_flashcards: int = 5) -> Optional[Dict[str, Any]]`: Gera flashcards para o tema especificado.

### Estrutura da API

#### Endpoint `/generate-flashcards`

- **Método**: `POST`
- **Descrição**: Gera flashcards personalizados com base no tema e número desejado.
- **Parâmetros de Entrada**:
  - `subject` (str): O tema dos flashcards.
  - `num_flashcards` (int): Número de flashcards desejados (padrão: 5).
- **Retorno**:
  - JSON contendo os flashcards gerados.

## Exemplo de Requisição

```json
{
  "subject": "História da Matemática e Finanças",
  "num_flashcards": 5
}
