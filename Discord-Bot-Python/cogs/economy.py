import discord
import settings
import peewee
import random
from discord.ext import commands
from models.account import Account

logger = settings.logging.getLogger(__name__)

class EconomyBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # @commands.Cog.listener()
    # async def on_message(self, message: discord.Message):
    #     await message.add_reaction("👍")
    
    @commands.command()
    async def balance(self,ctx):
        account = Account.fetch(ctx.message)
        await ctx.send(f"Your balance is: {account.amount}")
    
    
    @commands.command()
    async def coin(self, ctx, choice: str, amount: int):
        account = Account.fetch(ctx.message)
        
        if amount > account.amount:
            await ctx.send("You don't have enough credit!!")
            return 
        
        won = False
        heads = random.randint(0,1)
        if heads and choice.lower().startswith("h"):
            won = True
            account.amount += amount
        elif not heads and choice.lower().startswith("t"):
            won = True
            account.amount += amount
        else:
            account.amount -= amount
           
        account.save()
        
        message="You lost!"
        if won:
            message = "You won!"


        await ctx.send(f"{message}")
        
        
async def setup(bot):
    await bot.add_cog(EconomyBot(bot))
    