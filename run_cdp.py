import json, time, urllib.request

req = urllib.request.urlopen("http://localhost:9222/json/list")
tabs = json.loads(req.read().decode())
fb_tab = next(t for t in tabs if t.get("type") == "page")

ws_url = fb_tab["webSocketDebuggerUrl"]

# Simple CDP WebSocket navigation
import urllib.parse
page_url = "https://www.facebook.com/groups/1574365339447298/search/?q=cse231"
target_id = fb_tab["id"]

# Send navigate command via CDP HTTP endpoint if available or python websocket
print("Target tab:", fb_tab["title"], fb_tab["url"])
