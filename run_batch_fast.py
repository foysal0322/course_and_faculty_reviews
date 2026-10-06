import os
import sys
import time
import subprocess
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

sys.stdout.reconfigure(line_buffering=True)

courses = ["cse417", "cse401", "cse418", "cse426", "cse473"]

def get_driver():
    # Try attaching to existing Chrome on port 9222
    try:
        opt = Options()
        opt.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
        driver = webdriver.Chrome(options=opt)
        print("Connected to existing Chrome on port 9222.", flush=True)
        return driver
    except Exception as e:
        print(f"Debugger attach failed ({e}), launching Chrome Profile 2...", flush=True)
        chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
        if not os.path.exists(chrome_path):
            chrome_path = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
        cmd = [chrome_path, "--remote-debugging-port=9222", "--profile-directory=Profile 2"]
        subprocess.Popen(cmd)
        time.sleep(4)
        opt = Options()
        opt.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
        driver = webdriver.Chrome(options=opt)
        print("Launched and connected to Chrome Profile 2.", flush=True)
        return driver

driver = get_driver()

with open("raw/collector.js", encoding="utf-8") as f:
    collector_js = f.read()

for course in courses:
    out_file = f"raw/q_{course}.json"
    done_file = f"{out_file}.done"
    
    # Check if already has data
    if os.path.exists(done_file):
        if os.path.exists(out_file) and os.path.getsize(out_file) > 100:
            print(f"Skipping {course.upper()}: already completed ({out_file} has data).", flush=True)
            continue
        else:
            print(f"Cleaning stale empty done file for {course.upper()}...", flush=True)
            try: os.remove(done_file)
            except: pass

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
        time.sleep(4)
        poll_count += 1
        try:
            status = driver.execute_script(
                "const S=window.__fb; return S?{n:S.posts.length, running:S.running, done:S.done, saves:S.saves, log:S.log}:'no state';"
            )
            print(f"[{course.upper()}] Status ({poll_count}): {status}", flush=True)
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

print("\nAll requested course scrapings completed successfully!", flush=True)
