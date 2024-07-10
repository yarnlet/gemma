import os
import discord
import re
from json import load
from dotenv import load_dotenv
from discord.ext import commands
from requests import get

load_dotenv()

TOKEN = os.getenv("token") # get token from .env file


INTENTS = discord.Intents.all()



AUTHOR = "Zoe S. (yarnlet)"
REPO = "https://github.com/yarnlet/gemma"
VERSION = "1.0.1"

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
    clear()

    synced = await bot.tree.sync()
    print(f"Synced {synced} commands")

    print(f"Logged in as {bot.user.name} - {bot.user.id}")
    print(f"Ready to use!")
    print("")
    
bot.run(TOKEN)