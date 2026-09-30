import json
import selenium.webdriver

options = selenium.webdriver.ChromeOptions()
options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
driver = selenium.webdriver.Chrome(options=options)
driver.get("https://www.facebook.com/groups/1574365339447298/search/?q=cse231")
print("Navigated successfully to", driver.current_url)
