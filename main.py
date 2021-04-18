import discord, config
from discord.ext import commands

bot = commands.Bot(
    command_prefix=commands.when_mentioned_or("yas!", "//"),
    intents=discord.Intents.all(),
    owner_ids=[511655498676699136, 421698654189912064],
)
token = open("token.txt").read()


@bot.event
async def on_ready():
    print("ready")
    user = (await bot.fetch_channel(config.channel)).guild.get_member(config.user)
    print(f"Now tracking status of {user}")
    print(f"{user} is now {'offline' if not user.status == discord.Status.online else 'online'}")
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name=f"{user.name} be {'offline' if not user.status == discord.Status.online else 'online'}",
        ),
    )


cogs = ["jishaku", "status"]

for cog in cogs:
    try:
        bot.load_extension(cog)
    except Exception as e:
        print(e)

bot.run(token)
