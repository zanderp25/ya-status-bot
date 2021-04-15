import discord
from discord.ext import commands
import config

class Status(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def set_status(self,user):
        await self.bot.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching, 
                name=f"{user.name} be {'offline' if not user.status == discord.Status.online else 'online'}",
            ),
        )
        await (await self.bot.fetch_channel(config.channel)).send(
            embed=discord.Embed(
                title = f"{user.name} is now {'offline' if not user.status == discord.Status.online else 'online'}",
                color = discord.Color.red() if not user.status == discord.Status.online else discord.Color.green()
            )
        )

    @commands.command()
    async def status(self,ctx):
        user = (await self.bot.fetch_channel(config.channel)).guild.get_member(config.user)
        await ctx.send(
            embed = discord.Embed(
                title=f"{user.name} Status",
                description=f"{user.name} is now {'offline' if not user.status == discord.Status.online else 'online'}",
                color = discord.Color.red() if not user.status == discord.Status.online else discord.Color.green()
            )
        )
    
    @commands.Cog.listener(name="on_member_update")
    async def on_member_update(self,before,after):
        if before.id == config.user:
            if before.status != discord.Status.offline and after.status == discord.Status.offline:
                print("Offline!")
                await self.set_status(after)
            elif before.status != discord.Status.online and after.status == discord.Status.online:
                print("Online!")
                await self.set_status(after)
            

def setup(bot):
    bot.add_cog(Status(bot))