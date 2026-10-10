import os
import sys
import time
import json
import subprocess
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

COURSES = [
    "MKT202", "MKT330", "MKT337", "MKT344", "MKT355", "MKT382",
    "MKT412", "MKT417", "MKT450", "MKT460", "MKT465", "MKT470", "MKT475"
]
GROUP_ID = "241165482653333"

def is_logged_in(driver):
    try:
        txt = driver.find_element('tag name', 'body').text
        if "Log in" in txt or "Sign Up" in txt or "Forgotten account?" in txt:
            return False
        return True
    except:
        return False

def main():
    sys.stdout.reconfigure(line_buffering=True, encoding='utf-8')
    with open("raw/collector.js", "r", encoding="utf-8") as f:
        js_code = f.read()

    user_data_dir = r"C:\Users\Foysal\OneDrive\Desktop\course_and_faculty_reviews\selenium_data"
    chrome_cmd = f'start "" "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="{user_data_dir}" --disable-notifications --start-maximized "https://www.facebook.com"'
    
    print("Popping visible Chrome window directly onto your desktop...", flush=True)
    os.system(chrome_cmd)
    time.sleep(4)

    opts = Options()
    opts.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    driver = webdriver.Chrome(options=opts)

    print("Checking Facebook login status...", flush=True)
    if not is_logged_in(driver):
        print("Facebook login required! Waiting for login in visible Chrome window...", flush=True)
        for wait_idx in range(60):
            time.sleep(3)
            if is_logged_in(driver):
                print("Facebook session authenticated successfully!", flush=True)
                break
            if wait_idx % 5 == 0:
                print(f"Waiting for Facebook login... ({wait_idx*3}s elapsed)", flush=True)

    print("Opening data sink tab...", flush=True)
    driver.execute_script("window.open('http://127.0.0.1:8765/', 'fbsink')")
    time.sleep(2)

    for course in COURSES:
        out_name = f"marketing/q_{course.lower()}.json"
        search_url = f"https://www.facebook.com/groups/{GROUP_ID}/search/?q={course.lower()}"
        print(f"\n=======================================================", flush=True)
        print(f"Starting re-scraping for MKT course: {course} ({out_name})", flush=True)
        print(f"URL: {search_url}", flush=True)
        print(f"=======================================================", flush=True)
        
        driver.get(search_url)
        time.sleep(5)

        print(f"Injecting collector JS script into visible browser...", flush=True)
        res = driver.execute_script(js_code, out_name, 60)
        print(f"Collector script status: {res}", flush=True)

        for poll in range(120):
            time.sleep(15)
            try:
                fb_status = driver.execute_script("return window.__fb ? {running: window.__fb.running, done: window.__fb.done, count: window.__fb.posts.length, log: window.__fb.log} : null")
                if fb_status:
                    print(f"[{course}] Posts gathered so far: {fb_status['count']} | Running: {fb_status['running']} | Done: {fb_status['done']}", flush=True)
                    if fb_status.get("done") or not fb_status.get("running"):
                        print(f"Completed re-scraping for {course}. Saved dataset to {out_name}.", flush=True)
                        break
            except Exception as e:
                print(f"Polling check exception: {e}", flush=True)

        print(f"Waiting 2 minutes before starting next MKT course...", flush=True)
        time.sleep(120)

    print("\nAll Marketing courses re-scraped successfully inside marketing folder!", flush=True)

if __name__ == "__main__":
    main()
