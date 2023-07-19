import settings
import discord 
from discord.ext import commands
from discord import app_commands
    
logger = settings.logging.getLogger("bot")


class MyGroup(app_commands.Group):
    @app_commands.command()
    async def ping(self, interaction: discord.Integration):
        await interaction.response.send_message("Pong")
     
    @app_commands.command()
    async def ciao(self,interaction: discord.Interaction):
        await interaction.response.send_message(
            f"Ciao! {interaction.user.mention}", ephemeral=True
        )
        

def run():
    intents = discord.Intents.all()
    
    bot = commands.Bot(command_prefix="!", intents=intents)
    
    @bot.event 
    async def on_ready():
        logger.info(f"User: {bot.user} (ID: {bot.user.id})")

        
        await bot.load_extension(f"slashcmds.welcome")
        # mygroup = MyGroup(name="greetings", description="Welcomes users")
        # bot.tree.add_command(mygroup)

        bot.tree.copy_global_to(guild=settings.GUILD_ID)
        await bot.tree.sync(guild=settings.GUILD_ID)
      
    
  
      
    bot.run(settings.TOKEN, root_logger=True)

if __name__ == "__main__":
    run()