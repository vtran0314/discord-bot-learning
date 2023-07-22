import discord
from discord.ext import commands
from ranks.controller import Ranks
from messengers.discord import DiscordMessenger
from .bothandler import BotHandler

class RSBot(commands.Bot):
    #Dont wan't to overwrite constructor
    ranks : Ranks
    
    def initialise(self):
        discord_messenger = DiscordMessenger()
        bot_handler = BotHandler(self)
        self.ranks = Ranks(bot_handler, discord_messenger)
        
    async def process_message(self, message: discord.Message):
        await self.ranks.process_message(message)
        
    async def process_reaction(self, payload: discord.RawReactionActionEvent):
        await self.ranks.process_reaction(payload)
        
    