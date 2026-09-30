import selenium.webdriver

options = selenium.webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
options.add_argument("--remote-debugging-port=9222")
driver = selenium.webdriver.Chrome(options=options)
driver.get("https://www.facebook.com/groups/1574365339447298/search/?q=cse231")
print("Browser launched with debugger port 9222 and navigated to CSE231")
