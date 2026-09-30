import json, time, urllib.request
import selenium.webdriver

options = selenium.webdriver.ChromeOptions()
options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
driver = selenium.webdriver.Chrome(options=options)

collector_js = open("raw/collector.js", encoding="utf-8").read()
res = driver.execute_script(collector_js, "q_cse231.json", 150)
print("Collector script status:", res)

# Open fbsink tab if not open
driver.execute_script("window.open('http://127.0.0.1:8765/', 'fbsink');")
print("fbsink tab opened")
