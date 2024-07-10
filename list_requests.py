import os
from requests import get

DIR = "/list" # relative path
FULLDIR = os.getcwd() + DIR # full path
JS_PATH = "https://laylist.pages.dev/js"
DATA_PATH = "https://laylist.pages.dev/data"
LIST_PATH = "https://laylist.pages.dev/data/_list.json"

async def refresh_list():
    global DIR, FULLDIR
    
    routes_text = ""

    # grab laylist routes.js
    routes = get("https://laylist.pages.dev/js/routes.js")

    routes_text = routes.text
    
    # cut lines from routes.js
    lines = routes_text.split("\n")
    routes_list = []

    for line in lines:
        if not "import" in line:
            continue
        else:
            line_split = line.split("'")
            line = line_split[1]
            routes_list.append(line)