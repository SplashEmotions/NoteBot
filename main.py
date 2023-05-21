import discord
import configparser
from discord.ext import commands

config = configparser.ConfigParser()
config.read('config.txt')

discord_token:str = config.get('DEFAULT', 'discord_token')

activity_text = "SplashBot"

intents = discord.Intents.default()
intents.presences = True
intents.activities = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user.name} включен')

    activity = discord.Game(name=activity_text)
    await bot.change_presence(activity=activity)

bot.run(discord_token)