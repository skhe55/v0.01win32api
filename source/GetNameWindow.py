import psutil
import win32gui
import win32process

notepads = [item for item in psutil.process_iter() if item.name() == 'GTA5.exe']
print(notepads)
windows = []
pid = next(item for item in psutil.process_iter() if item.name() == 'GTA5.exe').pid

print(pid)  

def enum_window_callback(hwnd, pid):
    tid, current_pid = win32process.GetWindowThreadProcessId(hwnd)
    if pid == current_pid and win32gui.IsWindowVisible(hwnd):
        windows.append(hwnd)
   

def getNameWindow():
    win32gui.EnumWindows(enum_window_callback, pid)
    s = win32gui.GetWindowText(windows[0])
    return s

