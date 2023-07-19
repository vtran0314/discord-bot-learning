import random
import typing
import settings
import discord
from discord.ext import commands
    
logger = settings.logging.getLogger("bot")


def run():
    intents = discord.Intents.default()
    intents.message_content = True
    
    bot = commands.Bot(command_prefix="!", intents=intents)
    
    @bot.event 
    async def on_ready():
        logger.info(f"User: {bot.user} (ID: {bot.user.id})")

        #await bot.load_extension("slashcmds.welcome")

        # bot.tree.copy_global_to(guild=settings.GUILD_ID)
        # await bot.tree.sync(guild=settings.GUILD_ID)

        
    @bot.command()
    async def ping(ctx):
        embed = discord.Embed(
            colour=discord.Colour.dark_teal(),
            description="This is a description",
            title="This is the title"
        )
        embed.set_footer(text="this is the footer")
        embed.set_author(name="Maouque", url = "")
        
        #Small image on top right
        embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/1078399381226659961/1096251403984437278/greenNek0.jpg")
        
        #Big image 
        embed.set_image(url="https://cdn.discordapp.com/attachments/1078399381226659961/1101183284681134090/IMG_0202.png")
        embed.add_field(name="Github", value="https://github.com/vtran0314/")
        embed.add_field(name="CTF Challange", value = "https://calderadev.fly.dev")
        
        embed.insert_field_at(1, name = "LinkedIn", value ="https://www.linkedin.com/in/vinh-tran314/")
        
        await ctx.send(embed=embed)
          
    bot.run(settings.TOKEN, root_logger=True)

if __name__ == "__main__":
    run()