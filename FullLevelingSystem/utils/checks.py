import settings
from discord.ext import commands

def is_command_channel():
    def predicate(ctx):
        return ctx.message.channel.id == settings.COMMANDS_CH
    return commands.check(predicate)
        