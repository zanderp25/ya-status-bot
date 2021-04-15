import discord, config
from discord.ext import commands

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
                color = discord.Color.red() if not user.status == discord.Status.online else discord.Color.green()
            ).set_author(
                name=f"{user.name} is now {'offline' if not user.status == discord.Status.online else 'online'}", 
                icon_url=f"{user.avatar_url}"
            )
        )
    async def notify(self,user):
        users = [(await self.bot.fetch_channel(config.notif_channel)).guild.get_member(user).mention for user in config.notif_users]
        await (await self.bot.fetch_channel(config.notif_channel)).send(
            f'{", ".join(users)}: {user.name} is offline'
        )

    @commands.command()
    async def status(self,ctx):
        '''tests the status of the bot/user currently being tracked'''
        user = (await self.bot.fetch_channel(config.channel)).guild.get_member(config.user)
        await ctx.reply(
            embed = discord.Embed(
                description=f"{user.name} is {'offline' if not user.status == discord.Status.online else 'online'} right now.",
                color = discord.Color.red() if not user.status == discord.Status.online else discord.Color.green()
            ).set_author(
                name=f"{user.name}", 
                icon_url=f"{user.avatar_url}"
            )
        )
    @commands.command(name="notif-test", aliases=["notif","notiftest"])
    @commands.is_owner()
    async def test_notify(self,ctx):
        '''tests if the notifications work'''
        await self.notify(ctx.author)
        await ctx.reply("test notification sent")
    
    @commands.Cog.listener(name="on_member_update")
    async def on_member_update(self,before,after):
        if before.id == config.user:
            if before.guild == (await self.bot.fetch_channel(config.channel)).guild:
                if before.status == discord.Status.online and after.status != discord.Status.online:
                    print("Offline!")
                    await self.set_status(after)
                    await self.notify(before)
                elif before.status != discord.Status.online and after.status == discord.Status.online:
                    print("Online!")
                    await self.set_status(after)
            

def setup(bot):
    bot.add_cog(Status(bot))
