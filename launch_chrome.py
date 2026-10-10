import os
import subprocess

chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
url = "https://www.facebook.com"
profile = "Profile 2"

cmd = [chrome_path, f"--profile-directory={profile}", url]
subprocess.Popen(cmd, shell=False)
print("Launched Chrome on user screen.")
