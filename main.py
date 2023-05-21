import configparser
from discord.ext.commands import Bot
from discord.ext import commands
import asyncio
import time
import discord

config = configparser.ConfigParser()
config.read('config.txt')

discord_token = config.get('DEFAULT', 'discord_token')

Client = discord.Client()
bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print("Установка активности!") # увед. о начале работы

bot.run(discord_token) 