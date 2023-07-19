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
        
    
    '''
    NOTICE:
        The choice have a maximum of 25 so keep that in mind while developing 
    
    '''
    async def drink_autocompletion(
        interaction: discord.Interaction,
        current: str
    ) -> typing.List[app_commands.Choice[str]]:
        data = []
        for drink_choice in ['beer', 'milk', 'tea', 'coffee', 'juice']:
            if current.lower() in drink_choice.lower():
                data.append(app_commands.Choice(name=drink_choice, value=drink_choice))
        return data 

    @bot.tree.command()
    @app_commands.autocomplete(item=drink_autocompletion)
    async def drink(interaction: discord.Interaction, 
                    item: str
            ):
        await interaction.response.send_message(f"{item}", ephemeral=True)
    
    

  
    
    bot.run(settings.TOKEN, root_logger=True)

if __name__ == "__main__":
    run()