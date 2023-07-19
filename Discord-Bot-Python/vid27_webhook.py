import asyncio 
import discord 
from discord import Webhook
import aiohttp 

async def anything(url):
    async with aiohttp.ClientSession() as session:
        webhook = Webhook.from_url(url, session=session)
        embed = discord.Embed(title="https://calderadev.fly.dev", description="Maouque's CTF Challenge")
        await webhook.send(embed=embed, username="Maoque Hook")
        
if __name__ == "__main__":
    url = "https://discord.com/api/webhooks/1125623895672750140/p7ep4gz46h6Lc9SaFFtMGTTV7bWuKymVJaimilXDppxyh9JQE5Cu4akeqYkdJ9YyPYT5"

    loop = asyncio.new_event_loop()
    loop.run_until_complete(anything(url))
    loop.close()