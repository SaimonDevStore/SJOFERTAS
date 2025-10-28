import re
import logging
import os
import requests
from threading import Thread
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from bs4 import BeautifulSoup
from config import Config

# Configuração de logs
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Servidor HTTP mínimo para o Render
app = Flask(__name__)

@app.route('/')
def health_check():
    return '🤖 Bot está online e funcionando!', 200

@app.route('/health')
def health():
    return {'status': 'ok', 'bot': 'running'}, 200

def run_flask():
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)

class ProductExtractor:
    """Extrator simples e robusto de produtos"""
    
    @staticmethod
    def is_aliexpress_link(url):
        """Verifica se é link do AliExpress"""
        return 'aliexpress.com' in url.lower() or 's.click.aliexpress.com' in url.lower()
    
    @staticmethod
    def is_shopee_link(url):
        """Verifica se é link da Shopee"""
        return 'shopee.com.br' in url.lower() or 'shp.ee' in url.lower()
    
    @staticmethod
    def extract_product_data(url):
        """Extrai dados do produto de forma simples e robusta"""
        try:
            print(f"[Extrator] Processando URL: {url}")
            
            # Headers para simular navegador
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1'
            }
            
            # Faz requisição
            response = requests.get(url, headers=headers, timeout=20, allow_redirects=True)
            final_url = response.url
            
            if response.status_code != 200:
                print(f"[Extrator] Erro HTTP: {response.status_code}")
                return ProductExtractor._create_fallback(url)
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Detecta plataforma
            if ProductExtractor.is_aliexpress_link(final_url):
                return ProductExtractor._extract_aliexpress(soup, final_url)
            elif ProductExtractor.is_shopee_link(final_url):
                return ProductExtractor._extract_shopee(soup, final_url)
            else:
                return ProductExtractor._create_fallback(final_url)
                
        except Exception as e:
            print(f"[Extrator] Erro: {e}")
            return ProductExtractor._create_fallback(url)
    
    @staticmethod
    def _extract_aliexpress(soup, url):
        """Extrai dados do AliExpress"""
        try:
            # Nome do produto
            name = "Produto do AliExpress"
            
            # Tenta meta tags primeiro
            og_title = soup.find('meta', property='og:title')
            if og_title:
                title = og_title.get('content', '').strip()
                if title:
                    name = title.split('|')[0].split('-')[0].strip()
                    if len(name) > 80:
                        name = name[:80] + "..."
            
            # Se não encontrou, tenta title tag
            if name == "Produto do AliExpress":
                title_tag = soup.find('title')
                if title_tag:
                    title = title_tag.text.strip()
                    name = title.split('|')[0].split('-')[0].strip()
                    if len(name) > 80:
                        name = name[:80] + "..."
            
            # Imagem
            image_url = ""
            og_image = soup.find('meta', property='og:image')
            if og_image:
                image_url = og_image.get('content', '')
            
            # Preço (tenta extrair do HTML)
            price = "Consulte no site"
            price_patterns = [
                r'US\s?\$\s?([\d,\.]+)',
                r'R\$\s?([\d,\.]+)',
                r'"price":\s?"([\d,\.]+)"',
                r'price["\']?\s*:\s*["\']?([\d,\.]+)'
            ]
            
            for pattern in price_patterns:
                matches = re.findall(pattern, soup.get_text())
                if matches:
                    try:
                        price_value = float(matches[0].replace(',', ''))
                        if price_value > 0:
                            # Converte USD para BRL (taxa aproximada)
                            price_brl = price_value * 5.0
                            price = f"R$ {price_brl:.2f}".replace('.', ',')
                            break
                    except:
                        continue
            
            return {
                'name': name,
                'price': price,
                'installments': '',
                'image_url': image_url,
                'original_url': url,
                'delivery': 'Envio Internacional',
                'available': True
            }
            
        except Exception as e:
            print(f"[AliExpress] Erro na extração: {e}")
            return ProductExtractor._create_fallback(url)
    
    @staticmethod
    def _extract_shopee(soup, url):
        """Extrai dados da Shopee"""
        try:
            # Nome do produto
            name = "Produto da Shopee"
            
            # Tenta meta tags
            og_title = soup.find('meta', property='og:title')
            if og_title:
                title = og_title.get('content', '').strip()
                if title:
                    name = title.split('|')[0].split('-')[0].strip()
                    if len(name) > 80:
                        name = name[:80] + "..."
            
            # Imagem
            image_url = ""
            og_image = soup.find('meta', property='og:image')
            if og_image:
                image_url = og_image.get('content', '')
            
            # Preço
            price = "Consulte no site"
            price_patterns = [
                r'R\$\s?([\d,\.]+)',
                r'"price":\s?"([\d,\.]+)"'
            ]
            
            for pattern in price_patterns:
                matches = re.findall(pattern, soup.get_text())
                if matches:
                    try:
                        price_value = float(matches[0].replace('.', '').replace(',', '.'))
                        if price_value > 0:
                            price = f"R$ {price_value:.2f}".replace('.', ',')
                            break
                    except:
                        continue
            
            return {
                'name': name,
                'price': price,
                'installments': '',
                'image_url': image_url,
                'original_url': url,
                'delivery': 'Pronta Entrega | BR',
                'available': True
            }
            
        except Exception as e:
            print(f"[Shopee] Erro na extração: {e}")
            return ProductExtractor._create_fallback(url)
    
    @staticmethod
    def _create_fallback(url):
        """Cria resposta básica quando não consegue extrair dados"""
        platform = "AliExpress" if ProductExtractor.is_aliexpress_link(url) else "Shopee"
        delivery = "Envio Internacional" if platform == "AliExpress" else "Pronta Entrega | BR"
        
        return {
            'name': f'Produto do {platform}',
            'price': 'Consulte no site',
            'installments': '',
            'image_url': '',
            'original_url': url,
            'delivery': delivery,
            'available': True
        }

class TelegramBot:
    """Bot principal do Telegram - Versão Simplificada"""
    
    def __init__(self):
        """Inicializa o bot"""
        Config.validate()
        self.app = Application.builder().token(Config.TELEGRAM_BOT_TOKEN).build()
        self._setup_handlers()
    
    def _setup_handlers(self):
        """Configura os handlers de comandos e mensagens"""
        self.app.add_handler(CommandHandler("start", self.start_command))
        self.app.add_handler(CommandHandler("status", self.status_command))
        self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /start"""
        welcome_message = """
🤖 *Bot de Ofertas - Formatador Automático*

📌 *Como usar:*
Envie um link de produto da Shopee ou AliExpress e receba o anúncio formatado automaticamente!

✅ *Plataformas suportadas:*
• Shopee
• AliExpress

🚀 *Teste agora!*
        """
        await update.message.reply_text(welcome_message, parse_mode='Markdown')
    
    async def status_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /status"""
        status_message = "✅ *Bot Online e Funcionando!*\n\n"
        status_message += "🌐 Plataformas: Shopee, AliExpress\n"
        status_message += "⚡ Status: *Operacional*"
        
        await update.message.reply_text(status_message, parse_mode='Markdown')
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handler principal para mensagens"""
        message_text = update.message.text
        
        # Detecta URLs na mensagem
        urls = self._extract_urls(message_text)
        
        if not urls:
            return  # Ignora mensagens sem links
        
        # Processa o primeiro link encontrado
        await self._process_product_link(update, urls[0])
    
    async def _process_product_link(self, update: Update, url: str):
        """Processa um link de produto"""
        # Envia mensagem de processamento
        processing_msg = await update.message.reply_text("🔍 Extraindo dados do produto...")
        
        try:
            # Extrai dados do produto
            product_data = ProductExtractor.extract_product_data(url)
            
            if not product_data:
                await processing_msg.edit_text("❌ Erro ao extrair dados do produto.")
                return
            
            # Deleta mensagem de processamento
            await processing_msg.delete()
            
            # Monta mensagem formatada
            name = product_data.get('name', 'Produto')
            price = product_data.get('price', 'Consulte no site')
            delivery = product_data.get('delivery', '')
            image_url = product_data.get('image_url', '')
            
            # Escapa caracteres especiais no link
            escaped_url = url.replace('_', '\\_').replace('*', '\\*').replace('[', '\\[').replace('`', '\\`')
            
            # Formata mensagem
            message = f"*{name}* | _{delivery}_\n\n"
            message += f"💵 *{price}*\n\n"
            message += f"🎯 Link do produto:\n{escaped_url}"
            
            # Envia com imagem se disponível
            if image_url:
                try:
                    await update.message.reply_photo(
                        photo=image_url,
                        caption=message,
                        parse_mode='Markdown'
                    )
                except:
                    # Se falhar, envia só texto
                    await update.message.reply_text(message, parse_mode='Markdown')
            else:
                await update.message.reply_text(message, parse_mode='Markdown')
            
        except Exception as e:
            logger.error(f"Erro ao processar link: {e}")
            try:
                await processing_msg.delete()
            except:
                pass
            await update.message.reply_text("❌ Erro ao processar o link. Tente novamente.")
    
    def _extract_urls(self, text):
        """Extrai URLs de um texto"""
        url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        return re.findall(url_pattern, text)
    
    def run(self):
        """Inicia o bot"""
        # Inicia servidor HTTP em thread separada
        flask_thread = Thread(target=run_flask, daemon=True)
        flask_thread.start()
        logger.info("🌐 Servidor HTTP iniciado na porta {}".format(os.environ.get('PORT', 10000)))
        
        logger.info("🤖 Bot iniciado e aguardando mensagens...")
        self.app.run_polling(
            allowed_updates=Update.ALL_TYPES,
            timeout=30,
            read_timeout=30,
            write_timeout=30,
            connect_timeout=30,
            pool_timeout=30
        )

if __name__ == '__main__':
    try:
        bot = TelegramBot()
        bot.run()
    except Exception as e:
        logger.error(f"Erro ao iniciar o bot: {e}")
