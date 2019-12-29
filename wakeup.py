# bot.py
import os
import discord
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')

task = None

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

#Task to loop the guy in and out of the channel
async def wake_task(voice_channels, mentioned_member):
    for voice_channel in voice_channels:
        for member in voice_channel.members:
            if member.id == mentioned_member.id:
                i = 0
                while True:
                    if i == 0:
                        await member.move_to(voice_channels[0])
                        i = 1
                    else:
                        await member.move_to(voice_channels[1])
                        i = 0

@bot.command()
async def wake(ctx, mentioned_member: discord.Member):
    global task
    task = bot.loop.create_task(wake_task(ctx.guild.voice_channels, mentioned_member))

@bot.command()
async def stop(ctx):
    global task
    task.cancel()
    task = None

bot.run(token)