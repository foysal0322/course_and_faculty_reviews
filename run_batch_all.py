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
options.add_experimental_option("detach", True)

print("Launching Chrome WebDriver...", flush=True)
driver = webdriver.Chrome(options=options)

print("Opening local sink tab...", flush=True)
driver.get("http://127.0.0.1:8765/")
time.sleep(2)

with open("raw/collector.js", encoding="utf-8") as f:
    collector_js = f.read()

for course in courses:
    out_file = f"q_{course}.json"
    done_file = f"raw/{out_file}.done"
    
    if os.path.exists(done_file):
        print(f"Skipping {course}: already completed ({done_file} exists).", flush=True)
        continue
        
    search_url = f"https://www.facebook.com/groups/1574365339447298/search/?q={course}"
    print(f"\n==========================================", flush=True)
    print(f"Navigating for {course.upper()}: {search_url}", flush=True)
    driver.get(search_url)
    time.sleep(5)
    
    res = driver.execute_script(collector_js, out_file, 60)
    print(f"Collector script status for {course.upper()}: {res}", flush=True)
    
    driver.execute_script("window.open('http://127.0.0.1:8765/', 'fbsink');")
    
    while True:
        time.sleep(5)
        try:
            status = driver.execute_script(
                "const S=window.__fb; return S?{n:S.posts.length, running:S.running, done:S.done, saves:S.saves, log:S.log}:'no state';"
            )
            print(f"[{course.upper()}] Progress: {status}", flush=True)
            if status != 'no state' and (status.get('done') or not status.get('running')):
                print(f"Finished scraping for {course.upper()}!", flush=True)
                break
        except Exception as e:
            print(f"Polling error for {course.upper()}: {e}", flush=True)
            break

print("\nAll requested course scrapings completed successfully!", flush=True)
