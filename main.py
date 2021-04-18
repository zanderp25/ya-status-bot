import discord
import config
from discord.ext import commands

bot = commands.Bot(
    command_prefix=commands.when_mentioned_or("yas!", "//"),
    intents=discord.Intents(
        guilds=True,
        members=True,
        guild_messages=True,
        presences=True,
        reactions=True
    ),
    owner_ids=config.bot_owners,
)
token = open("token.txt").read()


@bot.event
async def on_ready():
    print("Ready! Logged in as", str(bot.user))
    scog = bot.get_cog("Status")
    if not scog:
        print("critical error - status cog was not loaded at runtime.")
        return
    user = scog.user(config.user)
    print(f"Now tracking status of {user}")
    print(f"{user} is now {scog.name_status(user.status)}")
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name=f"{user.name} be {scog.name_status(user.status)}",
        ),
    )


cogs = ["jishaku", "status"]

for cog in cogs:
    try:
        bot.load_extension(cog)
    except Exception as e:
        print(e)

bot.run(token)
