import random
import settings
import discord
from discord.ext import commands
from cogs.greetings import Greetings

logger=settings.logging.getLogger("bot")


class Slapper(commands.Converter):
    use_nicknames : bool 
    
    def __init__(self, *, use_nicknames) -> None:
        self.use_nicknames = use_nicknames
        
    async def convert(self, ctx, argument):
        someone = random.choice(ctx.guild.members)
        nickname = ctx.author
        if self.use_nicknames:
            nickname = ctx.author.nick
            
        return f"{nickname} slaps {someone} with {argument}"

class NotOwner(commands.CheckFailure):
    ...

def is_owner():
    async def predicate(ctx):
        if  ctx.author.id != ctx.guild.owner_id:
            raise NotOwner("Only Owner is allowed to run this command")
        return True
    return commands.check(predicate)


def run():
    intents = discord.Intents.default()
    intents.message_content = True
    intents.members = True
    
    bot = commands.Bot(command_prefix="!", intents=intents)
    
    @bot.event
    async def on_ready():
        logger.info(f"User: {bot.user} (ID: {bot.user.id})")
        
        # await bot.load_extension("cogs.greetings")
        
        for cmd_file in settings.CMDS_DIR.glob("*.py"):
            if cmd_file.name != "__init__.py":
                await bot.load_extension(f"cmds.{cmd_file.name[:-3]}")
        
        for cog_file in settings.COGS_DIR.glob("*.py"):
            if cog_file.name != "__init__.py":
                await bot.load_extension(f"cogs.{cog_file.name[:-3]}")
                
        await bot.tree.sync()
        
        
        print("-----------------------------")
    
    # @bot.command()
    # async def reload(ctx, cog: str):
    #     await bot.reload_extension(f"cogs.{cog.lower()}")
    
    # @bot.command()
    # async def load(ctx, cog: str):
    #     await bot.load_extension(f"cogs.{cog.lower()}")
    
    # @bot.command()
    # async def unload(ctx, cog: str):
    #     await bot.unload_extension(f"cogs.{cog.lower()}")
    
    
    # @bot.event    
    # async def on_command_error(ctx, error):
    #     if isinstance(error, commands.MissingRequiredArgument):
    #         await ctx.send("handler error globally")   
    
    
    @bot.hybrid_command(
        aliases=['p'],
        help = "This is help",
        description = "This is description", #SHow when !help + command is specify
        brief = "This is brief", #A quick brief when type !help without specific command
        enabled = True, #hide command from discord but still work
        hidden = True
    )
    async def ping(ctx):
        """Answer with pong"""
        #await ctx.send(f"pong {round(bot.latency * 1000)}ms")
        user =discord.utils.get(bot.guilds[0].members, nick="maouque")
        if user:
            await user.send("hello maouque")
    
    
        """This bot.tree.command() method below is great for return URL
        During CTF development
        
        """
    @bot.tree.command()
    async def ciao(interaction: discord.Interaction):
        """Answer with pong"""
        await interaction.response.send_message(f"Ciao! {interaction.user.mention}", ephemeral=True)
    
    
    # @bot.command()
    # @is_owner()
    # async def say(ctx, what = "WHAT?"): #what = "WHAT" default output
    #     await ctx.send(what)    
    
    # @say.error
    # async def say_error(ctx, error):
    #     if isinstance(error, NotOwner):
    #         await ctx.send("Permission denied")
    
    # @bot.command()
    # async def say2(ctx, *what): # *what = inherent? maybe
    #     await ctx.send(" ".join(what)) 
   
    # @bot.group()
    # async def math(ctx):
    #     if ctx.invoked_subcommand is None:
    #         await ctx.send(f"No, {ctx.subcommand_passed} does not belong to math")
        
    # @math.command()
    # async def add(ctx, one : int , two : int):
    #     await ctx.send(one + two)
    
    # @add.error    
    # async def add_error(ctx, error):
    #     if isinstance(error, commands.MissingRequiredArgument):
    #         await ctx.send("handler error locally")   
    
    # @math.command()
    # async def substract(ctx, one : int , two : int):
    #     await ctx.send(one - two)
    
    
    # @bot.command()
    # async def slap(ctx, reason : Slapper(use_nicknames=True) ):
    #     await ctx.send(reason)
    
    bot.run(settings.TOKEN, root_logger=True)
    
    
if __name__ == "__main__":
    run()