# GHS STUDIOS IA 🤖

> Um chatbot de código aberto alimentado por inteligência artificial com suporte a modelos gratuitos e pagos.

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.9%2B-brightgreen)]()
[![Status](https://img.shields.io/badge/status-Active%20Development-orange)]()

## 🌟 Características

- 🆓 **Suporte a IA Gratuita**: OpenAI GPT-3.5, Google Gemini Free, Hugging Face
- 💳 **Suporte a IA Paga**: OpenAI GPT-4, Claude (Anthropic), Cohere
- 🔌 **Integrações**: Discord, Telegram, Slack, Web Interface
- 🎨 **Interface Responsiva**: Web Dashboard moderno e intuitivo
- 📚 **Contexto Persistente**: Histórico de conversas e memória
- ⚙️ **Configurável**: Fácil customização de modelos e comportamentos
- 🔐 **Seguro**: Validação de entrada e gestão de chaves de API
- 📊 **Analytics**: Monitoramento de uso e performance

## 📋 Pré-requisitos

- Python 3.9+
- pip ou conda
- Uma chave de API (pelo menos uma IA gratuita ou paga)

## 🚀 Instalação Rápida

### 1. Clone o repositório
```bash
git clone https://github.com/brenograel41-jpg/hbc-studios-ia.git
cd hbc-studios-ia
```

### 2. Crie um ambiente virtual
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
```

### 4. Configure as variáveis de ambiente
```bash
cp .env.example .env
# Edite o arquivo .env com suas chaves de API
nano .env
```

### 5. Inicie o chatbot
```bash
python main.py
```

## 🎯 IAs Suportadas

### 🆓 Modelos Gratuitos

| Modelo | Provedor | Limite | Status |
|--------|----------|--------|--------|
| GPT-3.5 Turbo | OpenAI | 3 req/min | ✅ Ativo |
| Gemini | Google | 60 req/min | ✅ Ativo |
| Mistral | Hugging Face | Variável | ✅ Ativo |
| Llama 2 | Meta (HF) | Variável | ✅ Ativo |

### 💳 Modelos Pagos

| Modelo | Provedor | Preço | Status |
|--------|----------|-------|--------|
| GPT-4 | OpenAI | ~$0.03 | ✅ Ativo |
| Claude 3 | Anthropic | ~$0.01 | ✅ Ativo |
| Command | Cohere | ~$0.002 | ✅ Ativo |
| PaLM 2 | Google | ~$0.001 | ✅ Ativo |

## 📖 Uso

### Web Interface
```bash
python main.py --mode web
# Acesse http://localhost:5000
```

### Discord Bot
```bash
python main.py --mode discord
```

### Telegram Bot
```bash
python main.py --mode telegram
```

### CLI
```bash
python main.py --mode cli
```

## 🔧 Configuração

Edite o arquivo `.env`:

```env
# OpenAI
OPENAI_API_KEY=your_key_here
OPENAI_MODEL=gpt-4

# Google Gemini
GOOGLE_API_KEY=your_key_here

# Anthropic Claude
ANTHROPIC_API_KEY=your_key_here

# Telegram (opcional)
TELEGRAM_BOT_TOKEN=your_token_here

# Discord (opcional)
DISCORD_BOT_TOKEN=your_token_here

# Settings
DEFAULT_MODEL=gpt-3.5-turbo
MAX_HISTORY=50
TEMPERATURE=0.7
```

## 🤝 Contribuindo

Adoramos contribuições! Veja [CONTRIBUTING.md](./CONTRIBUTING.md) para detalhes sobre como:
- Reportar bugs
- Sugerir features
- Enviar pull requests

## 📝 Exemplos

### Python
```python
from src.bot import ChatBot

bot = ChatBot(model="gpt-4")
response = bot.chat("Qual é o significado da vida?")
print(response)
```

### Web API
```bash
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Olá!", "model": "gpt-3.5-turbo"}'
```

## 📊 Roadmap

- [ ] Suporte a visão por computador
- [ ] Análise de imagens
- [ ] Text-to-speech integrado
- [ ] Fine-tuning de modelos
- [ ] Dashboard de analytics avançado
- [ ] Sistema de plugins
- [ ] Suporte a múltiplos idiomas nativo

## 📄 Licença

Este projeto está licenciado sob a [MIT License](LICENSE).

## 📧 Contato & Suporte

- 📱 Issues: [GitHub Issues](https://github.com/brenograel41-jpg/hbc-studios-ia/issues)
- 💬 Discussions: [GitHub Discussions](https://github.com/brenograel41-jpg/hbc-studios-ia/discussions)

---

**Desenvolvido com ❤️ por GHS Studios**