import typing
import settings
import discord
import enum 
from discord.ext import commands
from discord import app_commands
    
logger = settings.logging.getLogger("bot")

def is_owner():
    def predicate(interaction: discord.Interaction):
        if interaction.user.id == interaction.guild.owner_id:
            return True
    return app_commands.check(predicate)

def run():
    intents = discord.Intents.all()
    
    bot = commands.Bot(command_prefix="!", intents=intents)
    
    @bot.event 
    async def on_ready():
        logger.info(f"User: {bot.user} (ID: {bot.user.id})")

        bot.tree.copy_global_to(guild=settings.GUILD_ID)
        await bot.tree.sync(guild=settings.GUILD_ID)
    
        
    @bot.tree.command()
    @is_owner()
    async def say(interaction: discord.Interaction, text_to_send: str):
        await interaction.response.send_message(
            f"{text_to_send}", ephemeral=False
        ) 

    @say.error
    async def say_error(interaction: discord.Interaction, error):
        await interaction.response.send_message("Not allowed!", ephemeral=False)

      
    bot.run(settings.TOKEN, root_logger=True)

if __name__ == "__main__":
    run()