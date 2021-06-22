from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox, QWidget
from simple_gui import Ui_MainWindow
from FishingBotApp import FishingBotApp
from list_Window_Names import list_window_names
from getnamesproc import getNameWindow
import sys, time
       


class Main_GUI(QtWidgets.QMainWindow):
    def __init__(self):
        super(Main_GUI, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.actionStart.triggered.connect(self.StartGame)
        self.ui.actionHelp.triggered.connect(self.Help)

    def StartGame(self):
        self.thread = QtCore.QThread()
        self.worker = FishingBotApp()
        self.worker.catching_on_bait_flag = True
        self.worker.NameHnwd = getNameWindow()#list_window_names()
        print(self.worker.NameHnwd)
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.RunninBot)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.worker.finished.connect(lambda:self.ui.label.setText('Finished.\nWaiting event...'))
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.start()
        self.ui.label.setText('Working.')

    def Help(self):
        msg = QtWidgets.QMessageBox()
        msg.setText("Для того чтобы бот начал свою работу, нажмите F4\nДля остановки бота нажмите клавишу F5.\n")
        msg.setWindowTitle("Help")   
        msg.setIcon(QMessageBox.Warning) 
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":main_icon"), QtGui.QIcon.Normal, QtGui.QIcon.Off) 
        msg.setWindowIcon(icon)
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)   
        msg.show()
        msg.exec_()

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    appl = Main_GUI()
    appl.show()

    sys.exit(app.exec())
