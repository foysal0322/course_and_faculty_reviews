import os, sys, time, json, urllib.request

SESSION_ID = "1fb42025-e96b-4015-804c-6032af47102f"
COURSES = ['MKT202', 'MKT330', 'MKT337', 'MKT344', 'MKT355', 'MKT382', 'MKT412', 'MKT417', 'MKT450', 'MKT460', 'MKT465', 'MKT470', 'MKT475']

os.makedirs("markating", exist_ok=True)

def open_page_mcp(url):
    nav_payload = {"url": url}
    req = urllib.request.Request(f"http://127.0.0.1:4444/session/{SESSION_ID}/url", data=json.dumps(nav_payload).encode("utf-8"), headers={"Content-Type": "application/json"})
    res = urllib.request.urlopen(req)
    return json.loads(res.read().decode("utf-8"))

def execute_js_mcp(script):
    exec_payload = {"script": script, "args": []}
    req = urllib.request.Request(f"http://127.0.0.1:4444/session/{SESSION_ID}/execute/sync", data=json.dumps(exec_payload).encode("utf-8"), headers={"Content-Type": "application/json"})
    res = urllib.request.urlopen(req)
    return json.loads(res.read().decode("utf-8"))

def get_collector_code(save_name):
    return f"""
const NAME = "{save_name}", MAX = 60;
delete window.__fb;
const S = window.__fb = {{posts: [], running: true, done: false, log: [], stop: false, name: NAME, saves: 0}};
const sleep = ms => new Promise(r => setTimeout(r, ms));
const rnd = (a, b) => a + Math.random() * (b - a);

const getSink = () => {{
  const w = window.open('', 'fbsink');
  try {{ if (w.location.href === 'about:blank') w.location = 'http://127.0.0.1:8765/'; }} catch (e) {{}}
  window.focus();
  return w;
}};

const sendToSink = (name, body) => {{
  try {{
    const s = getSink();
    if (s) s.postMessage({{name, body: typeof body === 'string' ? body : JSON.stringify(body)}}, '*');
  }} catch (e) {{}}
}};

const save = async () => {{
  sendToSink(S.name, S.posts);
  sendToSink(S.name + '.log', S.log);
  if (S.done) sendToSink(S.name + '.done', {{n: S.posts.length, time: new Date().toISOString(), log: S.log}});
}};

(async () => {{
  let noNew = 0;
  while (!S.stop && S.posts.length < MAX && noNew < 8) {{
    window.scrollBy(0, rnd(700, 1100));
    await sleep(rnd(1500, 2500));

    const moreBtns = Array.from(document.querySelectorAll('div[role="button"], span[role="button"]'))
      .filter(b => /view (more|\\d+)|more comments/i.test(b.innerText || ''));
    for (const b of moreBtns.slice(0, 5)) {{
      try {{ b.click(); }} catch(e) {{}}
      await sleep(rnd(300, 600));
    }}

    const cards = Array.from(document.querySelectorAll('div[role="feed"] > div, div[data-ad-preview="message"]'));
    let addedThisLoop = 0;
    for (const c of cards) {{
      const text = c.innerText || '';
      if (text.length < 30) continue;
      if (!S.posts.some(p => p.raw === text)) {{
        S.posts.push({{ raw: text, scrapedAt: new Date().toISOString() }});
        addedThisLoop++;
      }}
    }}
    if (addedThisLoop === 0) noNew++;
    else {{ noNew = 0; save(); }}
  }}
  S.done = true;
  save();
}})();
return "started scraper for " + NAME;
"""

for course in COURSES:
    c_lower = course.lower()
    save_name = f"markating/q_{c_lower}.json"
    search_url = f"https://www.facebook.com/groups/1574365339447298/search/?q={c_lower}"
    print(f"\n==========================================", flush=True)
    print(f"=== Starting {course} ({search_url}) ===", flush=True)
    print(f"==========================================", flush=True)

    try:
        open_page_mcp(search_url)
    except Exception as e:
        print(f"Nav err: {e}", flush=True)
    time.sleep(5)

    try:
        script = get_collector_code(save_name)
        res = execute_js_mcp(script)
        print(f"Collector launched for {course}: {res}", flush=True)
    except Exception as e:
        print(f"Launch err: {e}", flush=True)

    # Poll until done
    for check in range(60): # max 15 mins per course
        time.sleep(15)
        # Check sink for done status
        try:
            req_done = urllib.request.Request(f"http://127.0.0.1:8765/f/{save_name}.done")
            res_done = urllib.request.urlopen(req_done)
            done_info = json.loads(res_done.read().decode("utf-8"))
            print(f"[{course}] Scraping DONE! Total posts: {done_info.get('n', 0)}", flush=True)
            break
        except Exception:
            pass

        # Check count from sink
        try:
            req_count = urllib.request.Request(f"http://127.0.0.1:8765/f/{save_name}")
            res_count = urllib.request.urlopen(req_count)
            posts = json.loads(res_count.read().decode("utf-8"))
            print(f"[{course}] Progress: {len(posts)} posts collected...", flush=True)
        except Exception:
            print(f"[{course}] Collector running...", flush=True)

    # Save finalized file to disk
    try:
        req_file = urllib.request.Request(f"http://127.0.0.1:8765/f/{save_name}")
        res_file = urllib.request.urlopen(req_file)
        posts_data = json.loads(res_file.read().decode("utf-8"))
        with open(save_name, "w", encoding="utf-8") as f:
            json.dump(posts_data, f, ensure_ascii=False, indent=2)
        print(f"Saved {len(posts_data)} posts to {save_name}", flush=True)
    except Exception as e:
        print(f"Error finalizing {save_name}: {e}", flush=True)

    time.sleep(3)

print("\n==========================================", flush=True)
print("ALL MARKETING COURSES SCRAPING COMPLETED!", flush=True)
print("==========================================", flush=True)
