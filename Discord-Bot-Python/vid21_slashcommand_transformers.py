import typing
import settings
import discord
import enum 
from discord.ext import commands
from discord import app_commands
    
logger = settings.logging.getLogger("bot")

class SlapReason(typing.NamedTuple):
    reason : str
    
class SlapTransformer(app_commands.Transformer):
    async def transform(
        self, interaction: discord.Interaction,
        value: str
    ) -> SlapReason:
        return SlapReason(reason=f"*** {value} ***")


def run():
    intents = discord.Intents.all()
    
    bot = commands.Bot(command_prefix="!", intents=intents)
    
    @bot.event 
    async def on_ready():
        logger.info(f"User: {bot.user} (ID: {bot.user.id})")

        await bot.load_extension("slashcmds.welcome")

        bot.tree.copy_global_to(guild=settings.GUILD_ID)
        await bot.tree.sync(guild=settings.GUILD_ID)

        
    @bot.tree.command()
    async def slap(interaction: discord.Interaction, reason: app_commands.Transform[SlapReason, SlapTransformer]):
        await interaction.response.send_message(
            f"{reason}", ephemeral=False
        ) 

    @bot.tree.command()
    async def range(interaction: discord.Interaction, value: app_commands.Range[int, None, 10]):
        await interaction.response.send_message(
            f"{value}", ephemeral=False
        )
      
    bot.run(settings.TOKEN, root_logger=True)

if __name__ == "__main__":
    run()