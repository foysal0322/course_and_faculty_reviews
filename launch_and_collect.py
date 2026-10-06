import os
import sys
import time
import json
import urllib.request
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

sys.stdout.reconfigure(line_buffering=True)

courses = ["cse417", "cse401", "cse418", "cse426", "cse473"]

options = Options()
# Try connecting to debug port 9222 first if running, else launch with Profile 2
options.add_argument(r"--user-data-dir=C:\Users\Foysal\AppData\Local\Google\Chrome\User Data")
options.add_argument(r"--profile-directory=Profile 2")
options.add_experimental_option("detach", True)

print("Starting Chrome driver...", flush=True)
try:
    driver = webdriver.Chrome(options=options)
except Exception as err:
    print(f"Direct profile launch error: {err}. Retrying without user-data-dir...", flush=True)
    options2 = Options()
    options2.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=options2)

# Open sink tab
print("Opening localhost sink tab...", flush=True)
driver.get("http://127.0.0.1:8765/")
time.sleep(1)

with open("raw/collector.js", encoding="utf-8") as f:
    collector_js = f.read()

for course in courses:
    out_file = f"q_{course}.json"
    done_file = f"raw/{out_file}.done"
    
    if os.path.exists(done_file):
        print(f"Skipping {course} as {done_file} exists.", flush=True)
        continue
        
    search_url = f"https://www.facebook.com/groups/1574365339447298/search/?q={course}"
    print(f"\n==========================================", flush=True)
    print(f"Navigating to {course}: {search_url}", flush=True)
    driver.get(search_url)
    time.sleep(4)
    
    # Execute collector
    res = driver.execute_script(collector_js, out_file, 60)
    print(f"Collector script started for {course}: {res}", flush=True)
    
    driver.execute_script("window.open('http://127.0.0.1:8765/', 'fbsink');")
    
    while True:
        time.sleep(5)
        try:
            status = driver.execute_script(
                "const S=window.__fb; return S?{n:S.posts.length, running:S.running, done:S.done, saves:S.saves, log:S.log}:'no state';"
            )
            print(f"[{course}] Status: {status}", flush=True)
            if status != 'no state' and (status.get('done') or not status.get('running')):
                print(f"Completed scraping for {course}!", flush=True)
                break
        except Exception as e:
            print(f"Polling error for {course}: {e}", flush=True)
            break

print("\nBatch scraping completed for all target courses!", flush=True)
