import os
import sys
import time
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# HRM Courses inside the HR folder
COURSES = ["HRM340", "HRM360", "HRM370", "HRM380", "HRM450", "HRM470"]
GROUP_ID = "1574365339447298"  # NSU Faculty Course & Grade Analysis group

def main():
    sys.stdout.reconfigure(line_buffering=True)
    with open("raw/collector.js", "r", encoding="utf-8") as f:
        js_code = f.read()

    opts = Options()
    opts.add_argument('--user-data-dir=C:\\Users\\Foysal\\OneDrive\\Desktop\\course_and_faculty_reviews\\selenium_data')
    opts.add_argument('--disable-notifications')
    opts.add_argument('--start-maximized')
    
    print("Launching visible automated Chrome window for HRM re-scraping...", flush=True)
    driver = webdriver.Chrome(options=opts)

    print("Navigating to Facebook...", flush=True)
    driver.get("https://www.facebook.com")
    time.sleep(2)
    if os.path.exists("fb_cookies.json"):
        with open("fb_cookies.json", "r") as f:
            cookies = json.load(f)
        for c in cookies:
            if c.get("name") in ["c_user", "xs", "datr", "sb", "fr"]:
                try:
                    driver.add_cookie({"name": c["name"], "value": c["value"], "domain": ".facebook.com", "path": "/"})
                except Exception as e:
                    pass

    print("Opening data sink tab...", flush=True)
    driver.execute_script("window.open('http://127.0.0.1:8765/', 'fbsink')")
    time.sleep(2)

    for course in COURSES:
        out_name = f"HR/q_{course.lower()}.json"
        search_url = f"https://www.facebook.com/groups/{GROUP_ID}/search/?q={course.lower()}"
        print(f"\n=======================================================", flush=True)
        print(f"Starting re-scraping for HRM course: {course} ({out_name})", flush=True)
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

        print(f"Waiting 2 minutes before starting next HRM course...", flush=True)
        time.sleep(120)

    print("\nAll HRM courses re-scraped successfully inside HR folder!", flush=True)
    driver.quit()

if __name__ == "__main__":
    main()
