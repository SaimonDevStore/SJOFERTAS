# 🤖 Bot Telegram - Extrator de Ofertas Shopee & AliExpress

Bot automatizado para Telegram que extrai informações de produtos da **Shopee** e **AliExpress** automaticamente ao receber um link.

## 🎯 Funcionalidades

- ✅ Extração automática de dados de produtos
- ✅ **API oficial do AliExpress integrada** 🆕
- ✅ Detecção inteligente de plataforma (Shopee/AliExpress)
- ✅ Captura de imagem do produto
- ✅ Cálculo de parcelamento sem juros
- ✅ Identificação de tipo de entrega (Brasil/Internacional)
- ✅ **Geração automática de links de afiliado** 🆕
- ✅ Formatação otimizada para canais de ofertas
- ✅ Comandos administrativos
- ✅ Código modular e expansível

## 📋 Requisitos

- Python 3.8 ou superior
- Token de bot do Telegram (obtido com @BotFather)
- **Chaves da API do AliExpress** (opcional, mas recomendado)

## 🚀 Instalação Local

### 1. Clone ou baixe o projeto

```bash
cd "BOT TELEGRAM"
```

### 2. Instale as dependências

```bash
pip install -r requirements.txt
```

### 3. Configure o token do bot

Crie um arquivo `.env` na raiz do projeto:

```env
TELEGRAM_BOT_TOKEN=seu_token_aqui

# Configurações da API do AliExpress (opcional)
ALIEXPRESS_API_KEY=sua_api_key_aqui
ALIEXPRESS_SECRET_KEY=seu_secret_key_aqui
ALIEXPRESS_TRACKING_ID=seu_tracking_id_aqui

# Funcionalidades do Bot
ENABLE_INSTALLMENTS=true
ENABLE_COUPONS=true
ENABLE_CASHBACK=true
ENABLE_LINK_SHORTENER=false
ENABLE_ALIEXPRESS_API=true
```

**📝 Nota:** Se não configurar a API do AliExpress, o bot usará scraping tradicional como fallback.

### 4. Execute o bot

```bash
python main.py
```

## 📱 Como Usar

1. Inicie uma conversa com seu bot no Telegram
2. Envie o comando `/start` para ver as instruções
3. Envie um link de produto da Shopee ou AliExpress
4. Aguarde a extração automática dos dados!

### Comandos Disponíveis

- `/start` - Inicia o bot e mostra boas-vindas
- `/status` - Verifica se o bot está online
- `/plataformas` - Lista plataformas suportadas
- `/config` - Mostra configurações ativas
- `/ajuda` - Exibe ajuda detalhada

## 🌐 Deploy GRATUITO (24/7)

Siga este guia completo para colocar seu bot online **100% grátis** usando o **Render.com**.

---

## 📖 GUIA COMPLETO DE DEPLOY NO RENDER.COM

### ✅ Por que Render.com?

- ✅ 100% Gratuito (plano Free)
- ✅ 750 horas/mês gratuitas
- ✅ Deploy automático via Git
- ✅ Sem necessidade de cartão de crédito
- ✅ SSL/HTTPS automático
- ✅ Fácil configuração

### 🛠️ Passo 1: Preparar o Projeto

Crie um arquivo `Procfile` (sem extensão) na raiz do projeto com o seguinte conteúdo:

```
web: python main.py
```

### 🛠️ Passo 2: Criar Conta no Render

1. Acesse [https://render.com](https://render.com)
2. Clique em **"Get Started"** ou **"Sign Up"**
3. Faça login com GitHub (recomendado) ou crie uma conta com email

### 🛠️ Passo 3: Enviar Código para GitHub

Se ainda não tem o código no GitHub:

1. Acesse [https://github.com](https://github.com)
2. Crie um novo repositório (pode ser privado)
3. Siga as instruções para fazer upload dos arquivos:

```bash
git init
git add .
git commit -m "Initial commit - Bot Telegram"
git branch -M main
git remote add origin https://github.com/seu-usuario/seu-repositorio.git
git push -u origin main
```

⚠️ **IMPORTANTE:** Adicione um arquivo `.gitignore` para não enviar seu `.env`:

```
.env
__pycache__/
*.pyc
.venv/
venv/
```

### 🛠️ Passo 4: Criar Web Service no Render

1. No painel do Render, clique em **"New +"** → **"Web Service"**
2. Conecte seu repositório GitHub
3. Configure o serviço:

**Configurações Básicas:**
- **Name:** `bot-telegram-ofertas` (ou nome de sua preferência)
- **Region:** `Ohio (US East)` (mais próximo do Brasil)
- **Branch:** `main`
- **Runtime:** `Python 3`
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `python main.py`
- **Instance Type:** `Free`

### 🛠️ Passo 5: Configurar Variáveis de Ambiente

Na seção **"Environment Variables"**, adicione:

```
TELEGRAM_BOT_TOKEN = seu_token_aqui
ALIEXPRESS_API_KEY = sua_api_key_aqui
ALIEXPRESS_SECRET_KEY = seu_secret_key_aqui
ALIEXPRESS_TRACKING_ID = seu_tracking_id_aqui
ENABLE_INSTALLMENTS = true
ENABLE_COUPONS = true
ENABLE_CASHBACK = true
ENABLE_LINK_SHORTENER = false
ENABLE_ALIEXPRESS_API = true
```

⚠️ **Substitua os valores pelos dados reais do seu bot e API!**

### 🛠️ Passo 6: Deploy

1. Clique em **"Create Web Service"**
2. Aguarde o deploy (pode levar 2-5 minutos)
3. Quando aparecer **"Live"** em verde, seu bot está online! 🎉

### 🛠️ Passo 7: Manter o Bot Ativo 24h

O plano gratuito do Render **desliga o serviço após 15 minutos de inatividade**. Para manter ativo:

#### Opção 1: Usar um Serviço de Ping (Recomendado)

Use o **UptimeRobot** (gratuito):

1. Acesse [https://uptimerobot.com](https://uptimerobot.com)
2. Crie uma conta gratuita
3. Adicione um novo monitor:
   - **Monitor Type:** HTTP(s)
   - **Friendly Name:** Bot Telegram
   - **URL:** URL do seu serviço Render (ex: `https://bot-telegram-ofertas.onrender.com`)
   - **Monitoring Interval:** 5 minutos

#### Opção 2: Modificar o Código (Alternativa)

Adicione um endpoint HTTP simples para receber pings. No `main.py`, adicione no início:

```python
from flask import Flask
import threading

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot está online!"

def run_flask():
    app.run(host='0.0.0.0', port=10000)
```

E modifique a função `run()`:

```python
def run(self):
    # Inicia Flask em thread separada
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()
    
    logger.info("🤖 Bot iniciado e aguardando mensagens...")
    self.app.run_polling(allowed_updates=Update.ALL_TYPES)
```

Adicione `Flask==3.0.0` no `requirements.txt`.

---

## 🔧 Alternativas Gratuitas de Deploy

### 1. **Railway.app**
- 500 horas/mês grátis
- Deploy via GitHub
- [https://railway.app](https://railway.app)

### 2. **Fly.io**
- 3 VMs gratuitas
- Comando: `flyctl launch`
- [https://fly.io](https://fly.io)

### 3. **PythonAnywhere**
- Plano gratuito limitado
- Interface web simples
- [https://www.pythonanywhere.com](https://www.pythonanywhere.com)

### 4. **Replit**
- Editor online
- Deploy com um clique
- [https://replit.com](https://replit.com)

---

## 🔑 Como Obter Token do Telegram Bot

1. Abra o Telegram e procure por **@BotFather**
2. Envie o comando `/newbot`
3. Escolha um nome para seu bot (ex: "Ofertas Shopee Bot")
4. Escolha um username único (ex: "ofertas_shopee_bot")
5. Copie o **token** fornecido (formato: `123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11`)
6. Cole no arquivo `.env` ou nas variáveis de ambiente do Render

## 🔑 Como Obter Chaves da API do AliExpress

### Passo 1: Criar Conta de Desenvolvedor
1. Acesse [https://developers.aliexpress.com/](https://developers.aliexpress.com/)
2. Faça login com sua conta do AliExpress
3. Clique em **"Create App"**

### Passo 2: Configurar Aplicação
1. **App Name:** Nome do seu bot (ex: "Bot Telegram Ofertas")
2. **App Type:** Selecione **"Affiliate"**
3. **Description:** Descrição do seu bot
4. Aceite os termos e clique em **"Create"**

### Passo 3: Obter Chaves
Após criar a aplicação, você terá acesso a:
- **App Key** (`ALIEXPRESS_API_KEY`)
- **App Secret** (`ALIEXPRESS_SECRET_KEY`)
- **Tracking ID** (`ALIEXPRESS_TRACKING_ID`) - seu ID de afiliado

### Passo 4: Configurar no Bot
Adicione as chaves no arquivo `.env`:

```env
ALIEXPRESS_API_KEY=sua_app_key_aqui
ALIEXPRESS_SECRET_KEY=sua_app_secret_aqui
ALIEXPRESS_TRACKING_ID=seu_tracking_id_aqui
ENABLE_ALIEXPRESS_API=true
```

**💡 Dica:** Com a API configurada, o bot conseguirá:
- ✅ Extrair dados mais precisos dos produtos
- ✅ Gerar links de afiliado automaticamente
- ✅ Obter informações de comissão
- ✅ Funcionar de forma mais estável

---

## 🎨 Exemplo de Saída

```
Gabinete SuperFrame Cube Mid Tower ATX, ARGB, Vidro Temp, S Fonte e S Cooler | Pronta Entrega | BR

💵 R$ 334,00 em 6x de R$ 55,67 SEM JUROS

🎯 Link do produto:
https://shopee.com.br/product/123456789

📷 [Imagem do produto]
```

---

## 📝 Estrutura do Projeto

```
BOT TELEGRAM/
├── main.py                 # Bot principal
├── config.py              # Configurações
├── scraper_shopee.py      # Extrator Shopee
├── scraper_aliexpress.py  # Extrator AliExpress
├── aliexpress_api_client.py # Cliente API AliExpress 🆕
├── requirements.txt       # Dependências
├── .env                   # Variáveis de ambiente (não commitar!)
├── env_example.txt        # Exemplo de configuração 🆕
├── Procfile              # Configuração para deploy
└── README.md             # Esta documentação
```

---

## 🔮 Funcionalidades Futuras

- [ ] Suporte para Mercado Livre
- [ ] Suporte para Amazon Brasil
- [ ] Integração com APIs de cupons
- [ ] Integração com cashback (Méliuz, Picpay, etc)
- [ ] Encurtador de links customizado
- [ ] Histórico de preços
- [ ] Alertas de queda de preço
- [ ] Comparador de preços entre plataformas

---

## ❓ Solução de Problemas

### Bot não responde
- Verifique se o token está correto
- Confirme que o serviço está "Live" no Render
- Verifique os logs no Render Dashboard

### Erro ao extrair dados
- Alguns produtos podem ter proteção anti-scraping
- Tente com outro produto
- Verifique sua conexão com internet

### Serviço desliga sozinho
- Configure um monitor no UptimeRobot
- Plano gratuito do Render hiberna após inatividade

---

## 📧 Suporte

Para dúvidas ou problemas:
1. Verifique os logs no Render Dashboard
2. Teste localmente primeiro
3. Consulte a documentação do python-telegram-bot

---

## 📄 Licença

Este projeto é de código aberto. Use como quiser! 🚀

---

## 🎉 Pronto!

Seu bot agora está **online 24/7 de forma gratuita**!

Teste enviando um link de produto no Telegram. 🎊
