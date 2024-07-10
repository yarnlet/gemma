import os
import json
from requests import get

DIR = "/list"  # relative path
FULLDIR = os.getcwd() + DIR  # full path
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
        if "import" not in line:
            continue
        else:
            line_split = line.split("'")
            route = line_split[1]
            routes_list.append(route)
            
    # save routes_list to routes.txt
    with open(os.path.join(FULLDIR, "tree", "routes.txt"), "w") as f:
        for route in routes_list:
            f.write(route + "\n")
            
    # grab javascript of each route
    for route in routes_list:
        route_path = route[1:]  # Remove the leading '/'
        js = get(JS_PATH + route_path)
        script_path = os.path.join(FULLDIR, "scripts", route_path.replace("/pages/", ""))
        os.makedirs(os.path.dirname(script_path), exist_ok=True)
        with open(script_path, "w", encoding="utf-8") as f:
            f.write(js.text)

    # grab list json file
    list_response = get(LIST_PATH)
    with open(os.path.join(FULLDIR, "tree", "_list.json"), "w", encoding="utf-8") as f:
        f.write(json.dumps(list_response.json()))
        
    # dump levels with categories
    list_json = list_response.json()
    level_dict = {}
    last_category = "none_debug"
    level_dict[last_category] = {"points": 0, "levels": []}

    for level in list_json:
        if level[0] == "_":  # category indicator
            level_dict[level] = {"points": 0, "levels": []}
            last_category = level
        else:
            print("Getting level " + level + "...")
            level_request = get(DATA_PATH + "/" + level + ".json")
            level_dict[last_category]["levels"].append({level: level_request.json()})

    with open(os.path.join(FULLDIR, "tree", "levels.json"), "w", encoding="utf-8") as f:
        f.write(json.dumps(level_dict))
        
    print("Refreshed list files.")
    return "0"

async def get_levels():
    global FULLDIR
    
    with open(os.path.join(FULLDIR + "\\tree\\levels.json"), "r", encoding="utf-8") as f:
        levels = json.load(f)
        
    level_list = []
    for category in levels:
        for level_dict in levels[category]["levels"]:
            for level in level_dict:
                level_list.append(level)
                
    return level_list

async def get_level(level):
    global FULLDIR
    
    with open(os.path.join(FULLDIR + "\\tree\\levels.json"), "r", encoding="utf-8") as f:
        levels = json.load(f)
        
    for category in levels:
        for level_dict in levels[category]["levels"]:
            if level in level_dict:
                return level_dict[level]
                
    return "Level not found."

# Make sure to call refresh_list() in an appropriate place within your async environment
# await refresh_list()
