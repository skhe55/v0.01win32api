import psutil
import win32gui
import win32process

notepads = [item for item in psutil.process_iter() if item.name() == 'GTA5.exe']
print(notepads)
windows = []
pid = next(item for item in psutil.process_iter() if item.name() == 'GTA5.exe').pid

print(pid)  # 4764

def enum_window_callback(hwnd, pid):
    tid, current_pid = win32process.GetWindowThreadProcessId(hwnd)
    if pid == current_pid and win32gui.IsWindowVisible(hwnd):
        windows.append(hwnd)
   

# pid = 4416  # pid уже получен на предыдущем этапе
def getNameWindow():
    win32gui.EnumWindows(enum_window_callback, pid)
    s = win32gui.GetWindowText(windows[0])
    #print(s)
    return s

# if __name__ == "__main__":
#     s = yologame()
#     print(s)