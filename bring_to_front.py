import ctypes
import win32gui
import win32con

def bring_chrome_to_front():
    found = False
    def enum_windows_callback(hwnd, extra):
        nonlocal found
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd)
            class_name = win32gui.GetClassName(hwnd)
            if "Chrome" in class_name or "Facebook" in title or "Chrome" in title:
                print(f"Bringing to front: HWND={hwnd} | Title='{title}' | Class='{class_name}'")
                win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
                win32gui.ShowWindow(hwnd, win32con.SW_SHOWMAXIMIZED)
                try:
                    win32gui.SetForegroundWindow(hwnd)
                except Exception as e:
                    print("SetForegroundWindow note:", e)
                found = True

    win32gui.EnumWindows(enum_windows_callback, None)
    if not found:
        print("No matching Chrome windows found.")

if __name__ == '__main__':
    bring_chrome_to_front()
