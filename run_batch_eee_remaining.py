import os
import sys
import time
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

sys.stdout.reconfigure(line_buffering=True)

opt = Options()
opt.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
driver = webdriver.Chrome(options=opt)

courses = ["eee312", "eee321", "eee342", "eee361", "eee362", "eee363"]
with open("raw/collector.js", encoding="utf-8") as f:
    collector_js = f.read()

for course in courses:
    out_file = f"eee/q_{course}.json"
    search_url = f"https://www.facebook.com/groups/1574365339447298/search/?q={course}"
    print(f"\n==========================================", flush=True)
    print(f"Navigating for {course.upper()}: {search_url}", flush=True)
    driver.get(search_url)
    time.sleep(4)
    
    print(f"Injecting collector script for {course.upper()}...", flush=True)
    res = driver.execute_script(collector_js, out_file, 60)
    print(f"Collector script status for {course.upper()}: {res}", flush=True)
    
    try:
        driver.execute_script("window.open('http://127.0.0.1:8765/', 'fbsink');")
    except Exception as e:
        print(f"Sink tab open error: {e}", flush=True)
    
    poll_count = 0
    while True:
        time.sleep(5)
        poll_count += 1
        try:
            status = driver.execute_script(
                "const S=window.__fb; return S?{n:S.posts.length, running:S.running, done:S.done, saves:S.saves}:'no state';"
            )
            if poll_count % 3 == 0:
                print(f"[{course.upper()}] Status ({poll_count * 5}s): {status}", flush=True)
            if status != 'no state' and (status.get('done') or not status.get('running')):
                print(f"Finished scraping for {course.upper()}!", flush=True)
                break
            if status == 'no state' and poll_count > 3:
                print(f"Collector lost state for {course.upper()}, re-injecting...", flush=True)
                res = driver.execute_script(collector_js, out_file, 60)
                poll_count = 0
        except Exception as e:
            print(f"Polling error for {course.upper()}: {e}", flush=True)
            break
