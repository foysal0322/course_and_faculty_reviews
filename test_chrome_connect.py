import os, sys, time, subprocess
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def get_driver():
    try:
        opt = Options()
        opt.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
        driver = webdriver.Chrome(options=opt)
        print("Connected to port 9222")
        return driver
    except Exception as e:
        print(f"Debugger attach failed: {e}. Launching Chrome...")
        chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
        if not os.path.exists(chrome_path):
            chrome_path = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
        cmd = [chrome_path, "--remote-debugging-port=9222", "--profile-directory=Profile 2"]
        subprocess.Popen(cmd)
        time.sleep(5)
        opt = Options()
        opt.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
        driver = webdriver.Chrome(options=opt)
        print("Launched & connected to Chrome Profile 2.")
        return driver

d = get_driver()
print("Current URL:", d.current_url)
