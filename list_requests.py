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
            
    # save routes_list to routes.txt
    with open(FULLDIR + "\\tree\\routes.txt", "w") as f:
        for route in routes_list:
            f.write(route + "\n")
            
    # grab javascript of each route
    for route in routes_list:
        route = route[1:]
        js = get(JS_PATH + route)
        with open(FULLDIR + "\\scripts\\" + route.replace("/pages/", ""), "w", encoding="utf-8") as f:
            f.write(js.text)