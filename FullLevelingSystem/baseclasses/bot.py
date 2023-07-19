import discord
from discord.ext import commands
from ranks.controller import Ranks


class RSBot(commands.Bot):
    #Dont wan't to overwrite constructor
    ranks : Ranks
    
    def initialise(self):
        self.ranks = Ranks()
        
    async def process_message(self, message: discord.Message):
        await self.ranks.process_message(message)
        
    async def process_reaction(self, payload: discord.RawReactionActionEvent):
        await self.ranks.process_reaction(payload)
        
    