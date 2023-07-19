import typing
import settings
import discord
import enum 
from discord.ext import commands
from discord import app_commands
    
logger = settings.logging.getLogger("bot")

class Food(enum.Enum):
    apple = 1
    bunbo = 2
    pho = 3

def run():
    intents = discord.Intents.all()
    
    bot = commands.Bot(command_prefix="!", intents=intents)
    
    @bot.event 
    async def on_ready():
        logger.info(f"User: {bot.user} (ID: {bot.user.id})")

        bot.tree.copy_global_to(guild=settings.GUILD_ID)
        await bot.tree.sync(guild=settings.GUILD_ID)
        
    @bot.tree.command()
    @app_commands.describe(text_to_send="Saying....")
    @app_commands.rename(text_to_send="message")
    async def say(interaction: discord.Interaction, text_to_send: str):
        await interaction.response.send_message(
            f"{text_to_send}", ephemeral=True
        ) 
    
    @bot.tree.command()
    async def drink(interaction: discord.Interaction, choice: typing.Literal['beer', 'milk', 'tea', 'coffee', 'soda']):
        await interaction.response.send_message(
            f"{choice}", ephemeral=True
        ) 
    
    #This method using the declared class Food to extend choices
    #and its functionality
    @bot.tree.command()
    async def eat(interaction: discord.Interaction, choice: Food):
        await interaction.response.send_message(
            f"{choice}", ephemeral=True
        ) 
    
    @bot.tree.command()
    @app_commands.choices(choice=[
        app_commands.Choice(name="red", value="1"),
        app_commands.Choice(name="blue", value="2"),
        app_commands.Choice(name="green", value="3"),
    ])
    async def color(interaction: discord.Interaction, choice: app_commands.Choice[str]):
        await interaction.response.send_message(
            f"{choice}", ephemeral=True
        ) 

      
    bot.run(settings.TOKEN, root_logger=True)

if __name__ == "__main__":
    run()