import discord
import config
import asyncio
from discord.ext import commands


class Status(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @property
    def notification_channel(self) -> discord.TextChannel:
        return self.bot.get_channel(config.notif_channel)
    
    @property
    def status_channel(self) -> discord.TextChannel:
        return self.bot.get_channel(config.channel)

    def user(self, user_id: int) -> discord.Member:
        return self.notification_channel.guild.get_member(user_id)

    @staticmethod
    def name_status(status: discord.Status):
        if status == discord.Status.online:
            return "online"
        return "offline"

    async def set_status(self, user):
        await self.bot.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name=f"{user.name} be {self.name_status(user.status)}",
            ),
        )
        embed = discord.Embed(
            color=discord.Color.red() if user.status != discord.Status.online else discord.Color.green(),
        )
        embed.set_author(
            name=f"{user.name} is now {self.name_status(user.status)}.",
            icon_url=str(user.avatar_url_as(static_format="png"))  # NB: webp has less support than png
        )
        await self.status_channel.send(embed=embed)

    async def notify(self, user):
        users = [
            self.user(user).mention
            for user in config.notif_users
        ]
        await self.notification_channel.send(f'{", ".join(users)}: {user.name} is offline!')

    @commands.command()
    async def status(self, ctx):
        """tests the status of the bot/user currently being tracked"""
        user = self.user(config.user)
        embed = discord.Embed(
            description=f"{user.name} is {self.name_status(user.status)} right now.",
            color=discord.Color.red() if user.status != discord.Status.online else discord.Color.green(),
        )
        embed.set_author(name=f"{user.name}", icon_url=f"{user.avatar_url}")
        await ctx.reply(
            embed=embed
        )

    @commands.command(name="notif-test", aliases=["notif", "notiftest"])
    @commands.is_owner()
    async def test_notify(self, ctx):
        """tests if the notifications work"""
        await self.notify(ctx.author)
        await ctx.reply("test notification sent")

    @commands.command(name="clear", aliases=["purge"])
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx):
        if ctx.channel.id == config.channel:
            n = await ctx.channel.purge(
                limit=1000,
                check=lambda msg: msg.author is ctx.guild.me,
            )
            msg = await ctx.send(f"Deleted {len(n)} messages.")
            await msg.delete(delay=2)
            await ctx.message.delete(delay=2)
        else:
            await ctx.reply(
                f"This command can only be used in {self.notification_channel.mention}"
            )

    @commands.Cog.listener(name="on_member_update")
    async def on_member_update(self, before, after):
        if before.id == config.user:
            if before.guild == self.notification_channel.guild:
                if before.status == discord.Status.online and after.status != discord.Status.online:
                    await self.set_status(after)
                    await self.notify(before)
                elif before.status != discord.Status.online and after.status == discord.Status.online:
                    await self.set_status(after)


def setup(bot):
    bot.add_cog(Status(bot))
