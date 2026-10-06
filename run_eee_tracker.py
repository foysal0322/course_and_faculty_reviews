import os, sys, time, json, urllib.request

SESSION_ID = "8fa009e3-d917-4064-a0e7-a2dc79522039"
COURSES = ['EEE413', 'EEE414', 'EEE415', 'EEE461', 'EEE462', 'EEE464', 'EEE465', 'EEE422', 'EEE424', 'EEE426', 'EEE427', 'EEE428', 'EEE432', 'EEE433', 'EEE436', 'EEE453', 'EEE468', 'EEE331', 'EEE421', 'EEE423', 'EEE451', 'EEE471']

collector_js = open("raw/collector.js", encoding="utf-8").read()

os.makedirs("eee", exist_ok=True)

def mcp_open_page(url):
    payload = {"session_id": SESSION_ID, "url": url}
    req = urllib.request.Request("http://127.0.0.1:3000/call", data=json.dumps({
        "server": "selenium", "tool": "open_page", "args": payload
    }).encode("utf-8"), headers={"Content-Type": "application/json"})

def poll_collector_status():
    pass

for i, course in enumerate(COURSES):
    c_lower = course.lower()
    save_name = f"eee/q_{c_lower}.json"
    search_url = f"https://www.facebook.com/groups/1574365339447298/search/?q={c_lower}"
    print(f"\n==========================================", flush=True)
    print(f"[{i+1}/{len(COURSES)}] Processing {course}...", flush=True)
    print(f"==========================================", flush=True)

    # Note: Page navigation and script execution are performed via Selenium tool calls.
    done = False
    for check in range(60): # poll for up to 15 mins
        time.sleep(15)
        # Check sink server for done status
        try:
            req_done = urllib.request.Request(f"http://127.0.0.1:8765/f/{save_name}.done")
            res_done = urllib.request.urlopen(req_done)
            done_info = json.loads(res_done.read().decode("utf-8"))
            print(f"[{course}] Scraping COMPLETED! Total posts: {done_info.get('n', 0)}", flush=True)
            done = True
            break
        except Exception:
            pass

        # Check post count from sink server
        try:
            req_count = urllib.request.Request(f"http://127.0.0.1:8765/f/{save_name}")
            res_count = urllib.request.urlopen(req_count)
            posts = json.loads(res_count.read().decode("utf-8"))
            print(f"[{course}] Progress: {len(posts)} posts collected...", flush=True)
        except Exception:
            print(f"[{course}] Scraping in progress...", flush=True)

    # Save to disk file
    try:
        req_file = urllib.request.Request(f"http://127.0.0.1:8765/f/{save_name}")
        res_file = urllib.request.urlopen(req_file)
        posts_data = json.loads(res_file.read().decode("utf-8"))
        with open(save_name, "w", encoding="utf-8") as f:
            json.dump(posts_data, f, ensure_ascii=False, indent=2)
        print(f"Saved {len(posts_data)} posts to {save_name}", flush=True)
    except Exception as e:
        print(f"Note for {save_name}: {e}", flush=True)

    time.sleep(2)

print("\nALL EEE COURSES SCRAPING COMPLETED!", flush=True)
