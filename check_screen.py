import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

sys.stdout.reconfigure(line_buffering=True)

try:
    options = Options()
    options.add_experimental_option("detach", True)
    options.add_argument("--remote-debugging-port=9222")
    driver = webdriver.Chrome(options=options)
    print("URL:", driver.current_url, flush=True)
    print("Title:", driver.title, flush=True)
    driver.save_screenshot("browser_view.png")
    print("Screenshot saved to browser_view.png", flush=True)
except Exception as e:
    print(f"Error: {e}", flush=True)
