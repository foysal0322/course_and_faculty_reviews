import subprocess
import os
import sys
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

sys.stdout.reconfigure(line_buffering=True)

chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
if not os.path.exists(chrome_path):
    chrome_path = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"

url = "https://www.facebook.com/groups/1574365339447298/search/?q=cse417"

cmd = [chrome_path, "--remote-debugging-port=9222", "--profile-directory=Profile 2", url]
print(f"Launching Chrome with debug port 9222 and Profile 2: {cmd}", flush=True)
subprocess.Popen(cmd)
time.sleep(5)

try:
    opt = Options()
    opt.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    driver = webdriver.Chrome(options=opt)
    print("URL:", driver.current_url, flush=True)
    print("Title:", driver.title, flush=True)
    driver.save_screenshot("browser_view.png")
    print("Saved screenshot to browser_view.png", flush=True)
except Exception as e:
    print(f"Driver connection error: {e}", flush=True)
