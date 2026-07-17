"""
GHS STUDIOS IA - Telegram Bot Integration
"""

import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

from ..bot import ChatBot

logger = logging.getLogger(__name__)


class TelegramBot:
    """Telegram bot integration"""
    
    def __init__(self, token):
        self.token = token
        self.chatbot = ChatBot()
        
        self.app = Application.builder().token(token).build()
        
        self.app.add_handler(CommandHandler("start", self.start))
        self.app.add_handler(CommandHandler("help", self.help))
        self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.message))
    
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(
            "👋 Olá! Bem-vindo ao GHS STUDIOS IA!\n"
            "Sou um assistente inteligente com suporte a múltiplos modelos de IA."
        )
    
    async def help(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(
            "🤖 GHS STUDIOS IA\n/start - Iniciar\n/help - Ajuda\n"
            "Envie uma mensagem para conversar!"
        )
    
    async def message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        try:
            await context.bot.send_chat_action(update.effective_chat.id, "typing")
            user_message = update.message.text
            response = self.chatbot.chat(user_message)
            
            if len(response) > 4090:
                chunks = [response[i:i+4090] for i in range(0, len(response), 4090)]
                for chunk in chunks:
                    await update.message.reply_text(chunk)
            else:
                await update.message.reply_text(response)
        except Exception as e:
            logger.error(f"Telegram error: {e}")
            await update.message.reply_text(f"❌ Erro: {str(e)}")
    
    def start(self):
        logger.info("Iniciando Telegram bot...")
        self.app.run_polling()