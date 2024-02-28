import discord
import asyncio
import os
from discord.ext import commands
from dotenv import load_dotenv
from parsing import parsing

load_dotenv()

stop_flag = False

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
    while not stop_flag:
        msg1, msg2, msg3 = parsing()
        if msg3:
            await ctx.send(msg1)
            await ctx.send(msg2)
            await ctx.send(msg3)
        elif msg2:
            await ctx.send(msg1)
            await ctx.send(msg2)
        elif msg1:
            await ctx.send(msg1)
        await asyncio.sleep(300)

@bot.command()
async def stop(ctx):    
    global stop_flag
    stop_flag = True
    await ctx.send("Work stoped!")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith('!status'):
        await message.channel.send("I'm good!")

    await bot.process_commands(message)


bot.run(os.getenv('TOKEN'))
