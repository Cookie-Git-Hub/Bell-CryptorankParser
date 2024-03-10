import discord
import asyncio
import os
from discord.ext import commands
from logic import control


token = os.environ["TOKEN"]
stop_flag = False
amount_project = 10
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.command()
async def start(ctx):
    await ctx.send("I'm starting!")
    global stop_flag
    stop_flag = False
    while not stop_flag:
        try:
            msg = await control(amount_project)
            amount_pr = len(msg)
            for count in range(amount_pr):
                message = msg[count]
                await ctx.send(message)
        except Exception:
            print(f"No new projects or error occurred while parsing: {Exception}")
        await asyncio.sleep(120)


@bot.command()
async def stop(ctx):    
    global stop_flag
    stop_flag = True
    await ctx.send("Work stopped!")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith('!status'):
        await message.channel.send("I'm good!")

    await bot.process_commands(message)


bot.run(token)

