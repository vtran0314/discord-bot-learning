import settings
import discord
from discord.ext import commands

logger = settings.logging.getLogger("bot")


def run():
    intents = discord.Intents.all()

    bot = commands.Bot(command_prefix="!", intents=intents)

    @bot.event
    async def on_ready():
        logger.info(f"User: {bot.user} (ID: {bot.user.id})")
        
        logger.info(f"Guild ID: {bot.guilds[0].id}")
        
        bot.tree.copy_global_to(guild=settings.GUILD_ID)
        
        await bot.tree.sync(guild=settings.GUILD_ID)

    @bot.command()
    async def ping(ctx):
        await ctx.send("Pong")

   #@bot.tree.command(description="Welcome User", name="greetings", nsfw=True)
   #NOTICE: if the nsfw=True - the channel needs to set flag to age restricted
   #        or else it won't show up in the slashcommand.
   #        This method is used to hide shady shit 😎🤣
     
    @bot.tree.command(description="Welcome User", name="greetings")
    async def ciao(interaction: discord.Interaction):
        await interaction.response.send_message(
            f"Ciao! {interaction.user.mention}", ephemeral=True
        )

    bot.run(settings.TOKEN, root_logger=True)


if __name__ == "__main__":
    run()