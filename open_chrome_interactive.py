import ctypes
from ctypes import wintypes
import sys

class STARTUPINFO(ctypes.Structure):
    _fields_ = [
        ('cb', wintypes.DWORD),
        ('lpReserved', wintypes.LPWSTR),
        ('lpDesktop', wintypes.LPWSTR),
        ('lpTitle', wintypes.LPWSTR),
        ('dwX', wintypes.DWORD),
        ('dwY', wintypes.DWORD),
        ('dwXSize', wintypes.DWORD),
        ('dwYSize', wintypes.DWORD),
        ('dwXCountChars', wintypes.DWORD),
        ('dwYCountChars', wintypes.DWORD),
        ('dwFillAttribute', wintypes.DWORD),
        ('dwFlags', wintypes.DWORD),
        ('wShowWindow', wintypes.WORD),
        ('cbReserved2', wintypes.WORD),
        ('lpReserved2', ctypes.POINTER(ctypes.c_byte)),
        ('hStdInput', wintypes.HANDLE),
        ('hStdOutput', wintypes.HANDLE),
        ('hStdError', wintypes.HANDLE),
    ]

class PROCESS_INFORMATION(ctypes.Structure):
    _fields_ = [
        ('hProcess', wintypes.HANDLE),
        ('hThread', wintypes.HANDLE),
        ('dwProcessId', wintypes.DWORD),
        ('dwThreadId', wintypes.DWORD),
    ]

si = STARTUPINFO()
si.cb = ctypes.sizeof(STARTUPINFO)
si.lpDesktop = 'WinSta0\\Default'

pi = PROCESS_INFORMATION()

chrome_path = r'"C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://www.facebook.com'

res = ctypes.windll.kernel32.CreateProcessW(
    None,
    chrome_path,
    None,
    None,
    False,
    0,
    None,
    None,
    ctypes.byref(si),
    ctypes.byref(pi)
)

if res:
    print(f"Successfully launched Chrome on physical screen (WinSta0\\Default)! PID: {pi.dwProcessId}")
else:
    err = ctypes.GetLastError()
    print(f"CreateProcess failed with error: {err}")
