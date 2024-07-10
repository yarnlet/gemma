import os
import discord
import re
from time import time as dt
from json import load
from dotenv import load_dotenv
from discord.ext import commands
from requests import get

import list_requests as lr # local list request module

AUTHOR = "Zoe S. (yarnlet)"
REPO = "https://github.com/yarnlet/gemma"
VERSION = "1.0.1"

load_dotenv()
last_sync = ""
print(last_sync)

TOKEN = os.getenv("token") # get token from .env file
INTENTS = discord.Intents.all()

bot = commands.Bot(
    command_prefix="g ",
    intents=INTENTS,
    help_command=None,
    case_insensitive=True
)

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

@bot.event
async def on_ready():
    global last_sync
    
    clear()

    synced = await bot.tree.sync()
    print(f"Synced {len(synced)} commands")

    print(f"Logged in as {bot.user.name} - {bot.user.id}")
    print(f"Ready to use!")
    print("")

    last_sync = int(dt())
    await lr.refresh_list()
    
# sync bot's local files with the list files
@bot.hybrid_command(name="sync", description="Syncs the bot's local files with the list files.")
async def bot_sync(ctx):
    global last_sync

    if (int(dt()) - last_sync) < 30:
        return await ctx.send("The bot's files were synced less than 30 seconds ago. Please wait before syncing again. Last sync was at `" + str(last_sync) + "` or `" + str((int(dt()) - last_sync)) + "` seconds ago.")
    else:
        last_sync = int(dt())
        edits = await lr.refresh_list()
        return await ctx.send("Synced the bot's local files with the list files at ```" + str(last_sync) + "```. Made `" + str(len(edits)) + "` edits.")
        
    
bot.run(TOKEN)