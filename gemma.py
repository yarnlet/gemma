import os
import discord
import random
import typing
from time import time as dt
from json import loads, dumps
from dotenv import load_dotenv
from discord import app_commands
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
TEMP_PATH = os.getcwd() + "\\list\\temp\\"

bot = commands.Bot(
    command_prefix="g ",
    intents=INTENTS,
    help_command=None,
    case_insensitive=True
)

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

class Pagination(discord.ui.View):
    def __init__(self, pages: list):
        super().__init__()

        self.pages = pages
        self.current = 0

    @discord.ui.button(label="Previous", style=discord.ButtonStyle.blurple)
    async def previous(self, button: discord.ui.Button, interaction: discord.Interaction):
        if self.current > 0:
            self.current -= 1
            await interaction.response.edit_message(content=self.pages[self.current], view=self)

    @discord.ui.button(label="Next", style=discord.ButtonStyle.blurple)
    async def next(self, button: discord.ui.Button, interaction: discord.Interaction):
        if self.current < len(self.pages) - 1:
            self.current += 1
            await interaction.response.edit_message(content=self.pages[self.current], view=self)

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
    #await lr.refresh_list()
    
# sync bot's local files with the list files
@bot.tree.command()
async def sync(ctx: discord.Interaction):
    global last_sync

    if (int(dt()) - last_sync) < 30:
        return await ctx.response.send_message("The bot's files were synced less than 30 seconds ago. Please wait before syncing again. Last sync was at `" + str(last_sync) + "` or `" + str((int(dt()) - last_sync)) + "` seconds ago.")
    else:
        last_sync = int(dt())
        edits = await lr.refresh_list()
        return await ctx.response.send_message("Synced the bot's local files with the list files at ```" + str(last_sync) + "```. Made `" + str(len(edits)) + "` edits.")

@bot.tree.command()
async def level_stats(ctx: discord.Interaction, level: str):
    level_data = await lr.get_level(level)
    if level_data == "Level not found.":
        return await ctx.response.send_message("Level not found.")
    else:
        random_number = str(random.randint(0, 32767))
        with open(TEMP_PATH + level + "_" + random_number + ".json", "w", encoding="utf-8") as f: # possible problems with this line idk
            f.write(dumps(level_data))
            
        await ctx.response.send_message("Temporary json output for level " + level, file=discord.File(TEMP_PATH + level + "_" + random_number + ".json"))

        #delete the temporary file
        os.remove(TEMP_PATH + level + "_" + random_number + ".json")

@level_stats.autocomplete("level")
async def level_stats_autocomplete(interaction: discord.Interaction, current: str) -> typing.List[app_commands.Choice[str]]:
    data = []
    levels = await lr.get_levels()

    if current == "":
        first_ten_levels = levels[:10]  # first 10 levels
        for level in first_ten_levels:
            data.append(app_commands.Choice(name=level, value=level))
    else:
        for level in levels:
            if current.lower() in level.lower():
                data.append(app_commands.Choice(name=level, value=level))
    
    return data


    
    
bot.run(TOKEN)