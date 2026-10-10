import win32process
import win32con
import time
import subprocess

def launch():
    chrome_cmd = '"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:\\Users\\Foysal\\OneDrive\\Desktop\\course_and_faculty_reviews\\selenium_data" --disable-notifications https://www.facebook.com'
    si = win32process.STARTUPINFO()
    si.lpDesktop = r"WinSta0\Default"
    hProcess, hThread, dwProcessId, dwThreadId = win32process.CreateProcess(
        None,
        chrome_cmd,
        None,
        None,
        False,
        win32con.CREATE_NEW_CONSOLE,
        None,
        None,
        si
    )
    print(f"Spawned Chrome on WinSta0\\Default! PID: {dwProcessId}")

if __name__ == "__main__":
    launch()
