import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

sys.stdout.reconfigure(line_buffering=True)

opt = Options()
opt.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
d = webdriver.Chrome(options=opt)
print("TITLE:", d.title, flush=True)
print("URL:", d.current_url, flush=True)
feeds = d.find_elements("css selector", "[role=feed]")
print("FEEDS COUNT:", len(feeds), flush=True)
