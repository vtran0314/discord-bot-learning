import settings
import discord 
from discord.ext import commands
    
logger = settings.logging.getLogger("bot")

def run():
    intents = discord.Intents.default()
    intents.message_content = True
    intents.members = True
    
    bot = commands.Bot(command_prefix="!", intents=intents)
    
    @bot.event 
    async def on_ready():
        logger.info(f"User: {bot.user} (ID: {bot.user.id})")
        
        #bot.tree allow user to convert a command prefix ! to slashcommand /
        await bot.tree.sync()
    
    #hybrid command allow user to use both ! and / command of specify commands
    @bot.hybrid_command()
    async def pong(ctx):
        await ctx.send("ping")
        
    @bot.tree.command()
    async def ciao(interaction: discord.Interaction):
        await interaction.response.send_message(f"Ciao! {interaction.user.mention}", ephemeral=True)
      
    bot.run(settings.TOKEN, root_logger=True)

if __name__ == "__main__":
    run()