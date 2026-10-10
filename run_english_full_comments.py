import os, sys, time, json, urllib.request

SESSION_ID = "551f0d31-3bcc-4199-8653-949c21037dd4"
COURSES = ['ENG102', 'ENG103', 'ENG105', 'ENG111', 'ENG115', 'ENG210', 'ENG216', 'ENG220', 'ENG230', 'ENG307', 'ENG312', 'ENG337', 'ENG341', 'ENG346', 'ENG371', 'ENG381', 'ENG401', 'ENG417', 'ENG431', 'ENG458', 'ENG466', 'ENG481']

os.makedirs("English", exist_ok=True)

with open("raw/collector.js", "r", encoding="utf-8") as f:
    COLLECTOR_JS = f.read()

def call_selenium_mcp(tool_name, args_dict):
    url = "http://127.0.0.1:8765/mcp" # or call via native mcp tool interface if available
    # We will invoke selenium mcp via python subprocess calling node mcp or native http wrapper

for course in COURSES:
    c_lower = course.lower()
    save_name = f"English/q_{c_lower}.json"
    search_url = f"https://www.facebook.com/groups/1574365339447298/search/?q={c_lower}"
    print(f"\n==========================================", flush=True)
    print(f"=== Starting FULL COMMENT SCRAPING for {course} ({search_url}) ===", flush=True)
    print(f"==========================================", flush=True)
