import discord
import database
import settings
from discord.ext import commands
from baseclasses.bot import RSBot
from ranks.models import UserActivity
from users.models import User

def setup_tables():
    database.db.create_tables([User, UserActivity])

def run():
    setup_tables()
    intents = discord.Intents.all()
    #Use RSBot to handle all the command rather than use command.bot from discord
    #For readability
    bot = RSBot(command_prefix="!", intents=intents)
    bot.initialise()
    
    @bot.event
    async def on_ready():
        await bot.load_extension("ranks.cog")

    @bot.event
    async def on_message(message: discord.Message):
        #Handle experience only when message are send not commands.
        ctx = await bot.get_context(message)
        if not ctx.valid:
            if not message.author.bot:
                await bot.process_message(message)
        await bot.process_commands(message)

    @bot.event
    async def on_raw_reaction_add(payload: discord.RawReactionActionEvent):
        await bot.process_reaction(payload)

    @bot.event
    async def on_raw_reaction_remove(payload: discord.RawReactionActionEvent):
        await bot.process_reaction(payload)

    bot.run(settings.DISCORD_TOKEN)


if __name__ == "__main__":
    run()
