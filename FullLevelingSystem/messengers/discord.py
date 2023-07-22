import discord
import aiohttp
import settings
from baseclasses.messenger import Messenger

class DiscordMessenger(Messenger):
    async def send_message(self, message: str):
        async with aiohttp.ClientSession() as session:
            webhook = discord.Webhook.from_url(url=settings.CHATTER_HOOK,session=session)
            await webhook.send(message)