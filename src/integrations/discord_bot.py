"""
GHS STUDIOS IA - Discord Bot Integration
"""

import os
import logging
import discord
from discord.ext import commands

from ..bot import ChatBot

logger = logging.getLogger(__name__)


class DiscordBot(commands.Cog):
    """Discord bot integration"""
    
    def __init__(self, token):
        self.token = token
        self.chatbot = ChatBot()
        
        intents = discord.Intents.default()
        intents.message_content = True
        
        self.client = commands.Bot(command_prefix='!', intents=intents)
        self.client.add_cog(self)
        
        @self.client.event
        async def on_ready():
            logger.info(f"Discord bot: {self.client.user}")
        
        @self.client.event
        async def on_message(message):
            await self.handle_message(message)
    
    async def handle_message(self, message):
        if message.author == self.client.user:
            return
        
        await self.client.process_commands(message)
        
        if self.client.user.mentioned_in(message) or isinstance(message.channel, discord.DMChannel):
            async with message.channel.typing():
                try:
                    text = message.content.replace(f'<@{self.client.user.id}>', '').strip()
                    if not text:
                        return
                    
                    response = self.chatbot.chat(text)
                    
                    if len(response) > 2000:
                        chunks = [response[i:i+1990] for i in range(0, len(response), 1990)]
                        for chunk in chunks:
                            await message.reply(chunk, mention_author=False)
                    else:
                        await message.reply(response, mention_author=False)
                except Exception as e:
                    logger.error(f"Discord error: {e}")
                    await message.reply(f"❌ Erro: {str(e)}", mention_author=False)
    
    @commands.command(name='chat')
    async def chat_command(self, ctx, *, message):
        """!chat <mensagem>"""
        async with ctx.typing():
            try:
                response = self.chatbot.chat(message)
                if len(response) > 2000:
                    chunks = [response[i:i+1990] for i in range(0, len(response), 1990)]
                    for chunk in chunks:
                        await ctx.send(chunk)
                else:
                    await ctx.send(response)
            except Exception as e:
                await ctx.send(f"❌ Erro: {str(e)}")
    
    def run(self):
        self.client.run(self.token)