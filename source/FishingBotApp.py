from WindowCapture import WindowCapture
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
from GetNameWindow import getNameWindow
class FishingBotApp(QtCore.QObject):
    # Initialization of variables #
    # The colors we will be looking for in the game #
    # Circle Coord List - created for imitation clicks mouse on circle #
    NameHnwd = str()
    RButtonExpectedClr = (0, 0, 255)
    LButtonExpectedClr = (229, 229, 229)
    FinalNotificExpectedClr = (4,250,151)
    timeSleepingList = [0.011, 0.013, 0.015, 0.01, 0.02, 0.009]
    circleCoordList = [(738, 573), (745, 558), (749, 544), (761, 528), (767,515), (788, 506), (800, 495), (820, 488), 
                      (830, 486), (848, 494), (864, 498), (877, 506), (885, 518), (897, 532), (901, 547), (905, 564),
                      (907, 582), (909, 597), (906, 612), (900, 628), (888, 643), (879, 653), (857, 658), (840, 656),
                      (825, 657), (803, 651), (784, 645), (771, 633), (757, 619), (751, 611), (745, 601), (740, 589)]
    EndedBaitExpectedClr = (82, 0, 144)
    CaptchaExpectedClr = (61, 36, 248)
    catching_on_bait_flag = bool()
    finished = QtCore.pyqtSignal()

    # Waiting for user response to stop the bot #
    def waiting_response(self, delta):
            cur_time = datetime.datetime.now()
            new_time = cur_time + datetime.timedelta(seconds=delta)
            __exit = False
            while(datetime.datetime.now() < new_time):
                if keyboard.is_pressed('f5'):
                    __exit = True
                    break
                else:
                    __exit = False
            return __exit 

    # Bot implementation #
    # Screen capture, as well as all actions with the mouse and keyboard inside the game window are implemented using the win32api, pil, numpy tools. #
    # The bot works both in minimized / expanded mode. #
    def f_bot(self):
        wincap = WindowCapture(self.NameHnwd)
        _exit_flag_main_ = False
        _exit_flag_catching_cycle_ = False
        _finished_catching_flag_ = True
        while _exit_flag_main_ == False:
            _exit_flag_main_ = self.waiting_response(0.5)
            time.sleep(1)
            screenshot = wincap.get_screenshot()
            frame = Image.fromarray(screenshot)
            CaptchaActualClr = frame.getpixel((902, 582))
            if CaptchaActualClr == self.CaptchaExpectedClr:
                        playsound(os.path.abspath(os.curdir)[:-6] + 'resource/Alarm01.mp3')
            # catch a worm #
            elif _finished_catching_flag_ == True and _exit_flag_main_ == False and self.catching_on_bait_flag == False:
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
            # catch a bait #    
            elif _finished_catching_flag_ == True and _exit_flag_main_ == False and self.catching_on_bait_flag == True:
                win32gui.SendMessage(wincap.hwnd, win32con.WM_KEYDOWN, 0x37, 0)
                win32gui.SendMessage(wincap.hwnd, win32con.WM_KEYUP, 0x37, 0) 
                _finished_catching_flag_ = False
            time.sleep(1)
            # we track when the fishing rod starts to bite, and  start to pull out the fish, we check when it is possible to pull and when it is worth releasing the rod. #
            if _finished_catching_flag_ == False:
                while _exit_flag_catching_cycle_ == False:
                    if _exit_flag_catching_cycle_ == False:
                        _exit_flag_catching_cycle_ = self.waiting_response(0)
                        if _exit_flag_catching_cycle_ == True:
                            _exit_flag_main_ = True
                    i = 0
                    screenshot = wincap.get_screenshot()
                    frame = Image.fromarray(screenshot)
                    RButtonActualClr = frame.getpixel((1044, 875)) 
                    FinalNotificActualClr = frame.getpixel((650, 1021)) 
                    CaptchaActualClr = frame.getpixel((902, 582)) 
                    EndedBaitActualClr = frame.getpixel((649, 1001)) 
                    if RButtonActualClr == self.RButtonExpectedClr:
                        while RButtonActualClr == self.RButtonExpectedClr:
                            if i == 31:
                                i = 0
                            else:    
                                i += 1
                            # imitation mouse clicks on circle #
                            lParam = win32api.MAKELONG(self.circleCoordList[i][0], self.circleCoordList[i][1])
                            screenshot = wincap.get_screenshot()
                            frame_on_screen = Image.fromarray(screenshot)
                            RButtonActualClr = frame_on_screen.getpixel((1044, 875))
                            win32gui.SendMessage(wincap.hwnd, win32con.WM_SETCURSOR, wincap.hwnd, 1)
                            win32gui.SendMessage(wincap.hwnd, win32con.WM_MOUSEMOVE, 0x0000, lParam)
                            win32gui.SendMessage(wincap.hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lParam)
                            win32gui.SendMessage(wincap.hwnd, win32con.WM_LBUTTONUP, 0, lParam)
                            time.sleep(.1)
                    elif RButtonActualClr == self.LButtonExpectedClr:
                        print('Wait...')
                    elif EndedBaitActualClr == self.EndedBaitExpectedClr:
                        _finished_catching_flag_ = True
                        _exit_flag_main_ = True
                    elif FinalNotificActualClr == self.FinalNotificExpectedClr:
                        _finished_catching_flag_ = True
                        break             
        self.finished.emit()  
                
