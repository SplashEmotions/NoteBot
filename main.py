import configparser
import asyncio
import random
import time
import disnake
from disnake import OptionType, OptionChoice
from disnake.ext import commands
import pytz
from datetime import datetime

config = configparser.ConfigParser()
config.read('config.txt')

discord_token:str = config.get('DEFAULT', 'discord_token')


activity_text = "SplashBot"

intents = disnake.Intents.default()
intents.presences = True
intents.guilds = True

bot = commands.Bot(command_prefix="*", intents=disnake.Intents.all())

@bot.event
async def on_ready():
    print(f'{bot.user.name} включен')

@bot.command()
async def info(ctx):
    await ctx.send('Введите время:')
    time_msg = await bot.wait_for('message', check=lambda m: m.author == ctx.author)
    time_info = time_msg.content

    await ctx.send('Введите дату:')
    date_msg = await bot.wait_for('message', check=lambda m: m.author == ctx.author)
    date_info = date_msg.content

    await ctx.send('Введите текст:')
    text_msg = await bot.wait_for('message', check=lambda m: m.author == ctx.author)
    text_info = text_msg.content

    await ctx.send(f'Заметка сохранена:\nВремя: {time_info}\nДата: {date_info}\nТекст: {text_info}')

    # Получаем текущее время и дату в часовом поясе России
    current_datetime = datetime.now(pytz.timezone('Europe/Moscow'))
    current_time = current_datetime.strftime('%H:%M:%S')
    current_date = current_datetime.strftime('%Y-%m-%d')

    # Проверяем, совпадает ли текущее время и дата с заданными пользователем
    if current_time == time_info and current_date == date_info:
        await ctx.send(text_info)

bot.run(discord_token)
