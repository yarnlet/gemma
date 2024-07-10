from requests import get

routes = get("https://laylist.pages.dev/js/routes.js")

print(routes.text)