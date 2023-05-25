import configparser
import asyncio
import random
import time
import disnake
from disnake import OptionType, OptionChoice
from disnake.ext import commands
import pytz
from datetime import datetime, timedelta

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
async def schedule(ctx):
    await ctx.send('Введите время в формате ЧЧ:ММ (24-часовой формат):')
    time_msg = await bot.wait_for('message', check=lambda m: m.author == ctx.author)
    time_str = time_msg.content

    await ctx.send('Введите дату в формате ДД-ММ-ГГГГ:')
    date_msg = await bot.wait_for('message', check=lambda m: m.author == ctx.author)
    date_str = date_msg.content

    await ctx.send('Введите текст операции:')
    operation_msg = await bot.wait_for('message', check=lambda m: m.author == ctx.author)
    operation_text = operation_msg.content

    await ctx.send(f'Операция запланирована на {time_str} {date_str}')

    # Преобразуем время и дату в объект datetime
    scheduled_time = datetime.strptime(f'{date_str} {time_str}', '%d-%m-%Y %H:%M')

    # Функция, которая будет выполнена, когда наступит указанное время и дата
    async def execute_operation():
        await ctx.send(f'Операция выполнена: {operation_text}')

    # Функция для обновления времени по часовому поясу России
    async def update_time():
        while True:
            current_time = datetime.now(pytz.timezone('Europe/Moscow')).strftime('%H:%M:%S')
            await bot.change_presence(activity=disnake.Game(name=f"Current time in Russia (Moscow): {current_time}"))
            await disnake.utils.sleep_until(datetime.now() + timedelta(minutes=1))

    # Запускаем задачу обновления времени
    bot.loop.create_task(update_time())

    # Вычисляем время до выполнения операции
    delta = scheduled_time - datetime.now()

    # Запускаем таймер и выполняем операцию по истечении времени
    bot.loop.create_task(disnake.utils.sleep(delta.total_seconds()))
    bot.loop.create_task(execute_operation())

bot.run(discord_token)
