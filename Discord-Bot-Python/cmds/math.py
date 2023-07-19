from discord.ext import commands

@commands.group()
async def math(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.send(f"No, {ctx.subcommand_passed} does not belong to math")
    
@math.command()
async def add(ctx, one : int , two : int):
    await ctx.send(one + two)

@add.error    
async def add_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("handler error locally")   

@math.command()
async def substract(ctx, one : int , two : int):
    await ctx.send(one - two)
    
async def setup(bot):
    bot.add_command(math)