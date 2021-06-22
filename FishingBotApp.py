from WinCap import WindowCapture
import win32gui, win32ui, win32con, win32api
import cv2 as cv
import os
from PIL import Image
import time
import datetime
import keyboard
from random import randint
from playsound import playsound
from PyQt5 import QtCore
from list_Window_Names import list_window_names
from getnamesproc import getNameWindow
class FishingBotApp(QtCore.QObject):
    NameHnwd = str()
    Red_button_color = (0, 0, 255)
    White_button_color = (229, 229, 229)
    FinishedPanel_color = (4,250,151)#(98, 151, 6)
    timeSleepingList = [0.011, 0.013, 0.015, 0.01, 0.02, 0.009]
    cycleCoordList = [(738, 573), (745, 558), (749, 544), (761, 528), (767,515), (788, 506), (800, 495), (820, 488), 
                      (830, 486), (848, 494), (864, 498), (877, 506), (885, 518), (897, 532), (901, 547), (905, 564),
                      (907, 582), (909, 597), (906, 612), (900, 628), (888, 643), (879, 653), (857, 658), (840, 656),
                      (825, 657), (803, 651), (784, 645), (771, 633), (757, 619), (751, 611), (745, 601), (740, 589)]
    end_bait_logo_clr = (82, 0, 144)#(48, 0, 190)
    captcha_clr = (61, 36, 248)#(77, 53, 254)
    catching_on_bait_flag = bool()
    finished = QtCore.pyqtSignal()

    def make_screenshot(self, filename_all_img, filename_needle_img):
        full_img = cv.imread(filename_all_img, cv.IMREAD_UNCHANGED)
        needPart_img = cv.imread(filename_needle_img, cv.IMREAD_UNCHANGED)

        result_img = cv.matchTemplate(full_img, needPart_img, cv.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result_img)

        # print("Best match top left position: %s" % str(max_loc))
        # print("Best match confidence: %s" % max_val)
        m1 = max_loc[0]
        m2 = max_loc[1]
        return m1, m2, max_val
    

    def check_state(self, delta):
            cur_time = datetime.datetime.now()
            new_time = cur_time + datetime.timedelta(seconds=delta)
            __exit = False
            while(datetime.datetime.now() < new_time):
                if keyboard.is_pressed('f5'):
                    print("Work succesfull!")
                    __exit = True
                    break
                else:
                    __exit = False
            return __exit 

    def RunninBot(self):
        wincap = WindowCapture(self.NameHnwd)
        _exit_flag_main_ = False
        _exit_flag_catching_cycle_ = False
        _finished_catching_flag_ = True
        i = 0
        while _exit_flag_main_ == False:
            _exit_flag_main_ = self.check_state(0.5)
            time.sleep(1)
            screenshot = wincap.get_screenshot()
            frame_on_screen = Image.fromarray(screenshot)
            CaptchaClr = frame_on_screen.getpixel((915,605))#((902, 582))
            if CaptchaClr == self.captcha_clr:
                        playsound('Alarm01.mp3')
            elif _finished_catching_flag_ == True and _exit_flag_main_ == False and self.catching_on_bait_flag == False:
                # catch on worms, press 'i' and upload worm #
                lParam = win32api.MAKELONG(1733, 356)
                win32gui.SendMessage(wincap.hwnd, win32con.WM_KEYDOWN, 0x49, 0)
                win32gui.SendMessage(wincap.hwnd, win32con.WM_KEYUP, 0x49, 0)
                time.sleep(1)
                win32gui.SendMessage(wincap.hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lParam)
                win32gui.SendMessage(wincap.hwnd, win32con.WM_LBUTTONUP, 0, lParam)
                lParam = win32api.MAKELONG(1711, 485)
                time.sleep(1)
                win32gui.SendMessage(wincap.hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lParam)
                win32gui.SendMessage(wincap.hwnd, win32con.WM_LBUTTONUP, 0, lParam)
                _finished_catching_flag_ = False
            elif _finished_catching_flag_ == True and _exit_flag_main_ == False and self.catching_on_bait_flag == True:
                win32gui.SendMessage(wincap.hwnd, win32con.WM_KEYDOWN, 0x37, 0)
                win32gui.SendMessage(wincap.hwnd, win32con.WM_KEYUP, 0x37, 0) 
                _finished_catching_flag_ = False
            time.sleep(1)
            if _finished_catching_flag_ == False:
                while _exit_flag_catching_cycle_ == False:
                    if _exit_flag_catching_cycle_ == False:
                        _exit_flag_catching_cycle_ = self.check_state(0)
                        if _exit_flag_catching_cycle_ == True:
                            _exit_flag_main_ = True
                    i = 0
                    screenshot = wincap.get_screenshot()
                    frame_on_screen = Image.fromarray(screenshot)
                    RButtonClr = frame_on_screen.getpixel((1044, 895)) #((1044, 875))
                    FinalPanelClr = frame_on_screen.getpixel((651, 1014)) #((650, 1021))
                    CaptchaClr = frame_on_screen.getpixel((915, 605)) #((902, 582))
                    EndedBait = frame_on_screen.getpixel((651, 1014)) #((649, 1001))
                    if RButtonClr == self.Red_button_color:
                        while RButtonClr == self.Red_button_color:
                            if i == 31:
                                i = 0
                            else:    
                                i += 1
                            lParam = win32api.MAKELONG(self.cycleCoordList[i][0], self.cycleCoordList[i][1])
                            screenshot = wincap.get_screenshot()
                            frame_on_screen = Image.fromarray(screenshot)
                            RButtonClr = frame_on_screen.getpixel((1044, 895))#((1044, 875))
                            win32gui.SendMessage(wincap.hwnd, win32con.WM_SETCURSOR, wincap.hwnd, 1)
                            win32gui.SendMessage(wincap.hwnd, win32con.WM_MOUSEMOVE, 0x0000, lParam)
                            win32gui.SendMessage(wincap.hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lParam)
                            win32gui.SendMessage(wincap.hwnd, win32con.WM_LBUTTONUP, 0, lParam)
                            time.sleep(.1)
                    elif RButtonClr == self.White_button_color:
                        print('Wait...')
                    elif EndedBait == self.end_bait_logo_clr:
                        _finished_catching_flag_ = True
                        _exit_flag_main_ = True
                    elif FinalPanelClr == self.FinishedPanel_color:
                        _finished_catching_flag_ = True
                        break             
        self.finished.emit()  
                

    def CheckCoordColor(self):
        wincap = WindowCapture(self.NameHnwd)
        # m = self.make_screenshot('C:/Users/Sergey/Downloads/fishingBot_GTARP-main/OpenCvTestCase/cv_screen/end_worms.jpg', 'C:/Users/Sergey/Downloads/fishingBot_GTARP-main/OpenCvTestCase/cv_screen/end_worms_logo.jpg')
        # print(m)
        while True: 
            if keyboard.is_pressed('`'): break
            screen = wincap.get_screenshot()
            fr = Image.fromarray(screen)
            #fr.save('C:/Users/Sergey/Downloads/fishingBot_GTARP-main/OpenCvTestCase/new_pictures/end_bait.jpg')
            rB = fr.getpixel((651, 1014))
            print("RED - ", rB)            

# if __name__ == "__main__":
#     o = FishingBotApp()
#     #temp = list_window_names()
#     o.NameHnwd = yologame()#list_window_names()
#     print(o.NameHnwd)
#     o.CheckCoordColor()
#     o.catching_on_bait_flag = True
#     # s, s1, s2, s3, s4 = o.GetCoords()
#     # print(s, s1, s2, s3, s4)
#     # o.RunninBot()
  
# RED -  (64, 38, 252)