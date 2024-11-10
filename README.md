# Groq-Driven Educational Content API Suite

## Descrição

Este projeto contém uma suíte de APIs para geração de conteúdo educacional baseado em temas específicos, utilizando a API do Groq. Cada módulo oferece uma funcionalidade única para criação de materiais interativos, como flashcards, mapas mentais e caça-palavras.

### Módulos

1. **Flashcard Generator (`flashcardgenerator.py`)**: Gera flashcards personalizados sobre um tema fornecido.
2. **Mind Map Generator (`mindmapgenerator.py`)**: Cria mapas mentais que ilustram relações entre subtemas de um assunto.
3. **Word Search Generator (`wordsearchgenerator.py`)**: Constrói um caça-palavras com palavras relacionadas a um tema específico.

---

## Instalação e Configuração

1. **Instalar dependências**:
   ```bash
   pip install fastapi pydantic groq
   ```

2. **Configurar a chave da API**:
   Substitua o valor de `API_KEY` em cada módulo pelo seu valor de chave de API do Groq.

3. **Executar a API**:
   Use o comando abaixo para rodar cada módulo individualmente (substitua `nomemodulo` pelo nome do módulo, como `flashcardgenerator`, `mindmapgenerator` ou `wordsearchgenerator`):
   ```bash
   uvicorn nomemodulo:app --reload
   ```

---

## Estrutura e Documentação dos Módulos

### 1. Flashcard Generator

O `flashcardgenerator.py` é um módulo para gerar flashcards personalizados com base em um tema e quantidade especificados. Cada flashcard contém uma frente, verso, categoria, nível de dificuldade, tags, e uma imagem ilustrativa.

#### Classe `FlashcardGenerator`

- **Métodos**:
  - `__init__(api_key: str)`: Inicializa a classe com a chave de API do Groq.
  - `clean_response(response: str) -> str`: Corrige problemas de formatação na resposta da IA, especialmente com relação ao campo `id`.
  - `create_agent(role_name: str, initial_message: str) -> str`: Cria um agente na API Groq e obtém a resposta a partir de uma mensagem.
  - `create_flashcards(subject: str, num_flashcards: int = 5) -> Optional[Dict[str, Any]]`: Gera flashcards para um tema específico e retorna um dicionário JSON com o conteúdo.

#### Estrutura da API

- **Endpoint**: `/generate-flashcards`
  - **Método**: `POST`
  - **Descrição**: Gera flashcards personalizados com base no tema e no número de flashcards fornecido.
  - **Parâmetros de Entrada**:
    - `subject` (str): Tema dos flashcards.
    - `num_flashcards` (int): Número de flashcards desejados (padrão: 5).
  - **Retorno**: JSON contendo os flashcards gerados.

- **Exemplo de Requisição**:
  ```json
  {
    "subject": "História da Matemática e Finanças",
    "num_flashcards": 5
  }
  ```

---

### 2. Mind Map Generator

O `mindmapgenerator.py` é um módulo que gera mapas mentais com base em um tema, incluindo relações entre subtemas e o tema principal. Cada nó do mapa mental representa uma categoria ou subcategoria, e as conexões entre nós ilustram as relações hierárquicas.

#### Classe `MindMapGenerator`

- **Métodos**:
  - `__init__(api_key: str)`: Inicializa a classe com a chave de API do Groq.
  - `create_agent(role_name: str, initial_message: str) -> str`: Cria um agente na API Groq e obtém uma resposta a partir de uma mensagem.
  - `generate_mind_map(subject: str) -> Optional[Dict[str, Any]]`: Gera um mapa mental para um tema e retorna um dicionário JSON com os nós e conexões do mapa.

#### Estrutura da API

- **Endpoint**: `/generate-mind-map`
  - **Método**: `POST`
  - **Descrição**: Gera um mapa mental com base no tema fornecido.
  - **Parâmetros de Entrada**:
    - `subject` (str): Tema do mapa mental.
  - **Retorno**: JSON contendo o mapa mental, incluindo nós e conexões.

- **Exemplo de Requisição**:

```json
{
  "message": "Explique os fundamentos de cálculo",
  "temperature": 1.0,
  "max_tokens": 1024
}
```



---

### 3. Word Search Generator

O `wordsearchgenerator.py` é um módulo que gera caça-palavras com base em um tema fornecido. A API retorna uma grade com letras e as coordenadas das palavras relacionadas ao tema, criando uma experiência interativa de busca.

#### Classe `WordSearchGenerator`

- **Métodos**:
  - `__init__(api_key: str)`: Inicializa a classe com a chave de API do Groq.
  - `create_agent(role_name: str, initial_message: str) -> str`: Cria um agente na API Groq e obtém uma resposta a partir de uma mensagem.
  - `get_words_from_agent(topic: str, max_attempts: int = 3) -> List[str]`: Solicita uma lista de palavras relacionadas ao tema fornecido.
  - `place_word_in_grid(grid: List[List[str]], word: str) -> Optional[Dict[str, Any]]`: Insere uma palavra na grade do caça-palavras.
  - `generate_word_search(topic: str) -> Optional[Dict[str, Any]]`: Gera a grade de caça-palavras e retorna um dicionário JSON com a grade e posições das palavras.

#### Estrutura da API

- **Endpoint**: `/generate-word-search`
  - **Método**: `POST`
  - **Descrição**: Gera um caça-palavras com base no tema fornecido.
  - **Parâmetros de Entrada**:
    - `topic` (str): Tema do caça-palavras.
  - **Retorno**: JSON contendo a grade do caça-palavras e as posições das palavras.

- **Exemplo de Requisição**:
  ```json
  {
    "topic": "Ciência"
  }
  ```

---
Educational Assistant

O educationalassistant.py é um módulo projetado para interagir com os usuários em um formato conversacional, funcionando como um assistente educacional. O módulo utiliza um modelo avançado de linguagem para fornecer respostas detalhadas e contextualizadas baseadas nas interações do usuário.

### 4. Classe EducationalAssistant
- **Métodos:**
__init__(api_key: str): Inicializa a classe com a chave de API do Groq.
send_message(user_message: str, temperature: float = 1.0, max_tokens: int = 1024) -> str: Envia uma mensagem para a API e retorna a resposta do assistente.
clear_history(): Limpa o histórico de conversação do usuário, permitindo iniciar uma nova sessão de diálogo.
Estrutura da API
Endpoint: /send-message

### Método: POST
Descrição: Permite ao usuário enviar mensagens e receber respostas do assistente educacional.
Parâmetros de Entrada:
message (str): Mensagem do usuário.
temperature (float, opcional): Controla a criatividade das respostas.
max_tokens (int, opcional): Define o limite máximo de tokens para a resposta.
Retorno: JSON contendo a resposta do assistente.
Endpoint: /clear-history


Método: POST
Descrição: Limpa o histórico de conversação, permitindo ao usuário iniciar uma nova sessão de interação sem contexto anterior.
Exemplo de Requisição:

```json
{
  "message": "Explique os fundamentos de cálculo",
  "temperature": 1.0,
  "max_tokens": 1024
}
```

## Exemplos de Respostas das APIs

### Flashcard Generator

```json
{
  "general_subject": "História da Matemática e Finanças",
  "flashcards": [
    {
      "id": 1,
      "front": "Pergunta do flashcard",
      "back": "Resposta do flashcard",
      "category": "Categoria",
      "difficulty": "Nível de dificuldade",
      "tags": ["tag1", "tag2"],
      "image": "https://exemplo.com/imagem1.jpg"
    },
    ...
  ]
}
```

### Mind Map Generator

```json
{
  "general_subject": "História da Matemática",
  "nodes": [
    {"id": "1", "label": "História da Matemática", "type": "general_subject"},
    {"id": "2", "label": "Antiguidade", "type": "category", "parent": "1"},
    {"id": "3", "label": "Egito", "type": "sub_category", "parent": "2"}
  ],
  "edges": [
    {"source": "1", "target": "2"},
    {"source": "2", "target": "3"}
  ]
}
```

### Word Search Generator

```json
{
  "grid": [
    ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"],
    ["K", "L", "M", "N", "O", "P", "Q", "R", "S", "T"],
    ...
  ],
  "answers": [
    {"word": "CIÊNCIA", "start": [0, 0], "end": [0, 6]},
    {"word": "FÍSICA", "start": [1, 2], "end": [1, 7]}
  ]
}
```

---

## Testes e Validação

Para cada módulo, após configurar e executar a API, envie uma requisição POST para o endpoint correspondente usando os exemplos de requisição fornecidos. Verifique o retorno para assegurar que os dados estão formatados corretamente e que a API responde conforme esperado.

---

Este `README.md` fornece uma visão abrangente dos três módulos e seus respectivos endpoints, facilitando o entendimento e uso da API para geração de conteúdo educacional interativo.
```
