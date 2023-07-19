import discord
import settings
import database
from models.account import Account
from discord.ext import commands

logger = settings.logging.getLogger(__name__)

def run():
    
    database.db.create_tables([Account])
    
    intents = discord.Intents.all()
    
    bot = commands.Bot(command_prefix="!", intents=intents)
    
    @bot.event
    async def on_ready():
        logger.info(f"User: {bot.user} (ID: {bot.user.id})")
        logger.info(f"Bot is ready!")

        bot.tree.copy_global_to(guild=settings.GUILD_ID)
        await bot.tree.sync(guild=settings.GUILD_ID)
        
        await bot.load_extension("cogs.economy")
        
        
        
    bot.run(settings.TOKEN, root_logger=True)
    
if __name__ == "__main__":
    run()
    
    