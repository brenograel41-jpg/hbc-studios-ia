#!/usr/bin/env python3
"""
GHS STUDIOS IA - Main Entry Point
OpenSource AI Chatbot with Free and Paid Models Support
"""

import os
import sys
import logging
import argparse
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=os.getenv('LOG_LEVEL', 'INFO'),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Import modules
from src.bot import ChatBot
from src.web.app import create_app
from src.integrations.discord_bot import DiscordBot
from src.integrations.telegram_bot import TelegramBot


def run_cli_mode():
    """Run in CLI/Terminal mode"""
    logger.info("🤖 Starting GHS STUDIOS IA in CLI mode...")
    
    bot = ChatBot()
    print("\n" + "="*60)
    print("GHS STUDIOS IA - ChatBot CLI")
    print("="*60)
    print("Tipo 'exit' ou 'quit' para sair\n")
    
    while True:
        try:
            user_input = input("Você: ").strip()
            
            if user_input.lower() in ['exit', 'quit', 'sair']:
                print("\n👋 Até logo! Obrigado por usar GHS STUDIOS IA")
                break
            
            if not user_input:
                continue
            
            response = bot.chat(user_input)
            print(f"\n🤖 Assistente: {response}\n")
            
        except KeyboardInterrupt:
            print("\n\n👋 Interrompido pelo usuário")
            break
        except Exception as e:
            logger.error(f"Erro: {e}")
            print(f"❌ Erro: {e}\n")


def run_web_mode():
    """Run in Web mode"""
    logger.info("🌐 Starting GHS STUDIOS IA in Web mode...")
    
    app = create_app()
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('DEBUG', 'False').lower() == 'true'
    
    print("\n" + "="*60)
    print("GHS STUDIOS IA - Web Interface")
    print("="*60)
    print(f"🌐 Acesse: http://localhost:{port}")
    print("="*60 + "\n")
    
    app.run(host=host, port=port, debug=debug)


def run_discord_mode():
    """Run in Discord mode"""
    logger.info("📱 Starting GHS STUDIOS IA in Discord mode...")
    
    discord_token = os.getenv('DISCORD_BOT_TOKEN')
    if not discord_token:
        logger.error("❌ DISCORD_BOT_TOKEN não configurado em .env")
        sys.exit(1)
    
    bot = DiscordBot(token=discord_token)
    
    print("\n" + "="*60)
    print("GHS STUDIOS IA - Discord Bot")
    print("="*60)
    print("✅ Bot iniciado e conectado ao Discord")
    print("="*60 + "\n")
    
    bot.run()


def run_telegram_mode():
    """Run in Telegram mode"""
    logger.info("📞 Starting GHS STUDIOS IA in Telegram mode...")
    
    telegram_token = os.getenv('TELEGRAM_BOT_TOKEN')
    if not telegram_token:
        logger.error("❌ TELEGRAM_BOT_TOKEN não configurado em .env")
        sys.exit(1)
    
    bot = TelegramBot(token=telegram_token)
    
    print("\n" + "="*60)
    print("GHS STUDIOS IA - Telegram Bot")
    print("="*60)
    print("✅ Bot iniciado e aguardando mensagens no Telegram")
    print("="*60 + "\n")
    
    bot.start()


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='GHS STUDIOS IA - OpenSource AI Chatbot',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Exemplos de uso:
  python main.py                    # CLI mode (padrão)
  python main.py --mode web         # Web interface
  python main.py --mode discord     # Discord bot
  python main.py --mode telegram    # Telegram bot
  python main.py --mode all         # Todos os modos (experimental)
        '''
    )
    
    parser.add_argument(
        '--mode',
        choices=['cli', 'web', 'discord', 'telegram', 'all'],
        default='cli',
        help='Modo de operação (padrão: cli)'
    )
    
    parser.add_argument(
        '--config',
        type=str,
        help='Caminho para arquivo .env personalizado'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s 1.0.0'
    )
    
    args = parser.parse_args()
    
    # Load custom config if provided
    if args.config and os.path.exists(args.config):
        load_dotenv(args.config)
    
    logger.info("="*60)
    logger.info("🚀 GHS STUDIOS IA - Starting Up")
    logger.info("="*60)
    
    try:
        if args.mode == 'cli':
            run_cli_mode()
        elif args.mode == 'web':
            run_web_mode()
        elif args.mode == 'discord':
            run_discord_mode()
        elif args.mode == 'telegram':
            run_telegram_mode()
        elif args.mode == 'all':
            logger.warning("Modo 'all' ainda é experimental")
            run_cli_mode()
            
    except Exception as e:
        logger.error(f"❌ Erro fatal: {e}", exc_info=True)
        sys.exit(1)


if __name__ == '__main__':
    main()