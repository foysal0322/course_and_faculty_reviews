import os
import sys
import time
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

sys.stdout.reconfigure(line_buffering=True)

COURSES = ['INB350', 'INB372', 'INB400', 'INB410', 'INB480', 'INB490']

os.makedirs('INB', exist_ok=True)

def get_driver():
    for port in [50474, 9222]:
        try:
            opt = Options()
            opt.add_experimental_option("debuggerAddress", f"127.0.0.1:{port}")
            driver = webdriver.Chrome(options=opt)
            print(f"Successfully connected to Chrome on port {port}", flush=True)
            return driver
        except Exception:
            pass
    raise RuntimeError("Could not connect to Chrome debugger. Please make sure Chrome is running.")

driver = get_driver()

with open("raw/inb_collector.js", encoding="utf-8") as f:
    collector_js = f.read()

print(f"\n==========================================", flush=True)
print(f"Starting batch scrape for {len(COURSES)} INB courses...", flush=True)
print(f"Target directory: INB/", flush=True)
print(f"Courses: {', '.join(COURSES)}", flush=True)
print(f"==========================================", flush=True)

for idx, course in enumerate(COURSES, 1):
    c_lower = course.lower()
    save_path = f"INB/q_{c_lower}.json"
    
    if os.path.exists(save_path) and os.path.getsize(save_path) > 100:
        print(f"\n[{idx}/{len(COURSES)}] Skipping {course}: {save_path} already exists and has data.", flush=True)
        continue

    search_url = f"https://www.facebook.com/groups/1574365339447298/search/?q={c_lower}"
    print(f"\n==========================================", flush=True)
    print(f"[{idx}/{len(COURSES)}] Starting {course} ({search_url})", flush=True)
    print(f"==========================================", flush=True)

    try:
        driver.get(search_url)
    except Exception as e:
        print(f"[{course}] Navigation error: {e}", flush=True)
    
    time.sleep(6)

    try:
        res = driver.execute_script(collector_js, save_path, 200)
        print(f"[{course}] Scraper injected: {res}", flush=True)
    except Exception as e:
        print(f"[{course}] Script injection error: {e}", flush=True)
        continue

    start_time = time.time()
    last_log_time = time.time()
    
    while True:
        time.sleep(10)
        curr_time = time.time()
        
        try:
            status = driver.execute_script(
                "const S=window.__fb; return S ? {n: S.posts.length, running: S.running, done: S.done, saves: S.saves, log: S.log} : 'no state';"
            )
        except Exception as e:
            print(f"[{course}] Polling error: {e}", flush=True)
            status = 'no state'

        if curr_time - last_log_time >= 120 or (isinstance(status, dict) and status.get('done')):
            elapsed_min = round((curr_time - start_time) / 60, 1)
            if status != 'no state':
                posts_cnt = status.get('n', 0)
                is_done = status.get('done', False)
                logs = status.get('log', [])
                latest_log = logs[-1] if logs else 'N/A'
                print(f"[{course}] Check (elapsed {elapsed_min}m): {posts_cnt} posts collected. Status: {'DONE' if is_done else 'RUNNING'}. Last log: {latest_log}", flush=True)
            else:
                print(f"[{course}] Check (elapsed {elapsed_min}m): Collector state unavailable.", flush=True)
            last_log_time = curr_time

        if status != 'no state' and (status.get('done') or not status.get('running')):
            print(f"[{course}] Scraping completed!", flush=True)
            try:
                posts_data = driver.execute_script("return window.__fb ? window.__fb.posts : [];")
                with open(save_path, "w", encoding="utf-8") as out_f:
                    json.dump(posts_data, out_f, ensure_ascii=False, indent=2)
                print(f"[{course}] Successfully saved {len(posts_data)} posts to {save_path}", flush=True)
            except Exception as e:
                print(f"[{course}] Error saving posts: {e}", flush=True)
            break

        if curr_time - start_time > 1500:
            print(f"[{course}] Safety timeout reached (25 mins). Saving collected posts...", flush=True)
            try:
                posts_data = driver.execute_script("return window.__fb ? window.__fb.posts : [];")
                with open(save_path, "w", encoding="utf-8") as out_f:
                    json.dump(posts_data, out_f, ensure_ascii=False, indent=2)
                print(f"[{course}] Saved {len(posts_data)} posts to {save_path}", flush=True)
            except Exception as e:
                print(f"[{course}] Error saving on timeout: {e}", flush=True)
            break

print("\n==========================================", flush=True)
print("ALL 6 INB COURSES BATCH SCRAPING COMPLETED!", flush=True)
print("==========================================", flush=True)
