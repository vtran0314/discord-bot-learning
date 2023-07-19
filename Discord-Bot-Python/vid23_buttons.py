import settings
import discord
from discord.ext import commands
from discord import app_commands

logger = settings.logging.getLogger("bot")

class SimpleView(discord.ui.View):
    
    foo : bool = None
    
    async def disable_all_items(self):
        for item in self.children:
            item.disabled = True
        await self.message.edit_message(view=self)

            
    async def on_timeout(self) -> None:
        await self.message.channel.send("Timeout")
        await self.disable_all_items()
    
    @discord.ui.button(label="Start", style=discord.ButtonStyle.success)
    async def Start(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Starting challenge")
        self.foo = True
        self.stop()
    
    @discord.ui.button(label="Stop", style=discord.ButtonStyle.red)
    async def Stop(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Stopping challenge")
        self.foo = False
        self.stop()
        
    @discord.ui.button(label="Restart", style=discord.ButtonStyle.blurple)
    async def Restart(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Restarting challenge")
        self.stop()
        
def run():
    intents = discord.Intents.default()
    intents.message_content = True
    
    bot = commands.Bot(command_prefix="!", intents=intents)
    
    @bot.event 
    async def on_ready():
        logger.info(f"User: {bot.user} (ID: {bot.user.id})")
        logger.info(f"Bot is ready!")
        

        #await bot.load_extension("slashcmds.welcome")

        # bot.tree.copy_global_to(guild=settings.GUILD_ID)
        # await bot.tree.sync(guild=settings.GUILD_ID)

        
    @bot.tree.command()
    async def button(self, interaction : discord.Interaction):
        view = SimpleView(timeout=60)
        # button = discord.ui.Button(label="Start")
        # view.add_item(button)
        
        '''
        When we use on_timeout function above
        the interaction.response.message_send will not work
        therefore we need to create a self.interaction method
        '''
        message = await interaction.response.send_message(f"",view=view, ephemeral=True)
        view.message = message
        
        #Wait for button interaction
        await view.wait()
        
        #Disable button after interaction
        await view.disable_all_items()
        
        if view.foo is None:
            logger.error("Timeout")
        elif view.foo is True:
            logger.error("Ok")
        else:
            logger.error("Stopped")
         
    bot.run(settings.TOKEN, root_logger=True)

if __name__ == "__main__":
    run()