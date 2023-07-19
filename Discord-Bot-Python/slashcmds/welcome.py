import discord
from discord import app_commands

class MyGroup(app_commands.Group):
    @app_commands.command()
    async def ping(self, interaction: discord.Integration):
        await interaction.response.send_message("Pong")
     
    @app_commands.command()
    async def ciao(self,interaction: discord.Interaction):
        await interaction.response.send_message(
            f"Ciao! {interaction.user.mention}", ephemeral=True
        )

async def setup(bot):
    bot.tree.add_command(MyGroup(name="greeting2", description="Welcome user2 v2"))