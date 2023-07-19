import settings
import discord 
from discord.ext import commands
from discord import app_commands
    
logger = settings.logging.getLogger("bot")


def run():
    intents = discord.Intents.all()
    
    bot = commands.Bot(command_prefix="!", intents=intents)
    
    @bot.event 
    async def on_ready():
        logger.info(f"User: {bot.user} (ID: {bot.user.id})")

        bot.tree.copy_global_to(guild=settings.GUILD_ID)
        await bot.tree.sync(guild=settings.GUILD_ID)
    
         
    @bot.tree.context_menu(name="Show join date")
    async def get_joined_date(interaction: discord.Interaction, member: discord.Member):
        await interaction.response.send_message(
            f"Member joined {discord.utils.format_dt(member.joined_at)}", ephemeral=True
        )
        
    @bot.tree.context_menu(name="Report message")
    async def report_message(interaction: discord.Interaction, message: discord.Message):
        await interaction.response.send_message(
            f"message reported", ephemeral=True
        ) 
    
    
    #Channel cannot work in this case. Check the next vid18 
        
    # @bot.tree.context_menu(name="Voice Channel")
    # async def voice_channel(interaction: discord.Interaction, channel: discord.VoiceChannel):
    #     await interaction.response.send_message(
    #         f"message reported", ephemeral=True
    #     ) 
      
    bot.run(settings.TOKEN, root_logger=True)

if __name__ == "__main__":
    run()