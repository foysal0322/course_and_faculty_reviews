import sys
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

sys.stdout.reconfigure(line_buffering=True)

options = Options()
options.add_experimental_option("detach", True)
options.add_argument("--remote-debugging-port=9222")

driver = webdriver.Chrome(options=options)
url = "https://www.facebook.com/groups/1574365339447298/search/?q=cse417"
print(f"Navigating to {url}...", flush=True)
driver.get(url)
time.sleep(5)
print("Current Title:", driver.title, flush=True)
print("Current URL:", driver.current_url, flush=True)
driver.save_screenshot("browser_view.png")
print("Saved browser_view.png", flush=True)
