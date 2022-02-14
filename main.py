import enum
import sys
import win32api
import win32con
import threading
import time
from PyQt5 import QtCore
from PyQt5.QtWidgets import *
import settingsManager
from random import randint

settings = settingsManager.getSettings()


class MouseButton(enum.Enum):
    Left = "Left"
    Right = "Right"


class MouseDetector:
    @staticmethod
    def __convertButtonState__(state):
        if state < 0:
            return True
        else:
            return False

    def isLeftDown(self):
        return self.__convertButtonState__(win32api.GetKeyState(0x01))

    def isRightDown(self):
        return self.__convertButtonState__(win32api.GetKeyState(0x02))

    def isWhatDown(self, button):
        if button == MouseButton.Left:
            return self.__convertButtonState__(win32api.GetKeyState(0x01))
        else:
            return self.__convertButtonState__(win32api.GetKeyState(0x02))


class KeyDetector:
    @staticmethod
    def __equalCheck__(character):
        lowerCharacter = character.lower()
        upperCharacter = character.upper()

        checkResult = win32api.GetAsyncKeyState(ord(lowerCharacter))
        if not checkResult:
            checkResult = win32api.GetAsyncKeyState(ord(upperCharacter))

        return checkResult

    @staticmethod
    def __convertButtonState__(state):
        if state < 0:
            return True
        else:
            return False

    def isWhatDown(self, character):
        return self.__convertButtonState__(self.__equalCheck__(character))


def __randomisedBeforeDelay__():
    time.sleep(randint(settings['Randomisation']['BeforeClick']['Min'],
                       settings['Randomisation']['BeforeClick']['Max']) / 1000)


def __randomisedHoldDelay__():
    time.sleep(
        randint(settings['Randomisation']['HoldClick']['Min'], settings['Randomisation']['HoldClick']['Max']) / 1000)


def __sendClick__(buttonUp, buttonDown):
    win32api.mouse_event(buttonUp, win32api.GetCursorPos()[0], win32api.GetCursorPos()[1])
    __randomisedBeforeDelay__()
    win32api.mouse_event(buttonDown, win32api.GetCursorPos()[0], win32api.GetCursorPos()[1])
    __randomisedHoldDelay__()
    win32api.mouse_event(buttonUp, win32api.GetCursorPos()[0], win32api.GetCursorPos()[1])


class DoubleClicker:
    def __init__(self):
        self.leftClicked = False
        self.leftSimulatedClicks = 0
        self.leftEnabled = True
        self.leftKeyPressed = False

        self.rightClicked = False
        self.rightSimulatedClicks = 0
        self.rightEnabled = True
        self.rightKeyPressed = False

        self.thread = threading.Thread(target=self.__updateLoop__)
        self.threadStarted = False

        self.mouseDetector = MouseDetector()
        self.keyDetector = KeyDetector()

    def __toggleLeft__(self):
        if self.leftEnabled:
            self.leftEnabled = False
        else:
            self.leftEnabled = True

    def __toggleRight__(self):
        if self.rightEnabled:
            self.rightEnabled = False
        else:
            self.rightEnabled = True

    def __update__(self):
        self.leftClicked = self.mouseDetector.isLeftDown()
        self.rightClicked = self.mouseDetector.isRightDown()

        if settings['Buttons']['Left'] and self.leftEnabled:
            if self.leftClicked:
                if self.leftSimulatedClicks < randint(settings['DoubleClicks']['Min'], settings['DoubleClicks']['Max']):
                    self.leftSimulatedClicks += 1
                    __sendClick__(win32con.MOUSEEVENTF_LEFTUP, win32con.MOUSEEVENTF_LEFTDOWN)
                else:
                    self.leftSimulatedClicks = 0

        if settings['Buttons']['Right'] and self.rightEnabled:
            if self.rightClicked:
                if self.rightSimulatedClicks < randint(settings['DoubleClicks']['Min'], settings['DoubleClicks']['Max']):
                    self.rightSimulatedClicks += 1
                    __sendClick__(win32con.MOUSEEVENTF_RIGHTUP, win32con.MOUSEEVENTF_RIGHTDOWN)
                else:
                    self.rightSimulatedClicks = 0

        if self.keyDetector.isWhatDown(settings['Keybinds'][MouseButton.Left.value]) and not self.leftKeyPressed:
            self.leftKeyPressed = True
            self.__toggleLeft__()
        elif not self.keyDetector.isWhatDown(settings['Keybinds'][MouseButton.Left.value]) and self.leftKeyPressed:
            self.leftKeyPressed = False

        if self.keyDetector.isWhatDown(settings['Keybinds'][MouseButton.Right.value]) and not self.rightKeyPressed:
            self.rightKeyPressed = True
            self.__toggleRight__()
        elif not self.keyDetector.isWhatDown(settings['Keybinds'][MouseButton.Right.value]) and self.rightKeyPressed:
            self.rightKeyPressed = False

    def __updateLoop__(self):
        while True:
            self.__update__()
            time.sleep(0.001)

    def startThread(self):
        self.thread = threading.Thread(target=self.__updateLoop__)
        self.thread.start()
        self.threadStarted = True

    def stopThread(self):
        self.thread.join()
        self.threadStarted = False

    def isLeftEnabled(self):
        if settings['Buttons'][MouseButton.Left.value] and self.leftEnabled:
            return True
        return False

    def isRightEnabled(self):
        if settings['Buttons'][MouseButton.Right.value] and self.rightEnabled:
            return True
        return False

    def isWhatEnabled(self, button):
        if button == MouseButton.Left or button == MouseButton.Left.value:
            if settings['Buttons'][MouseButton.Left.value] and self.leftEnabled:
                return True
            return False
        else:
            if settings['Buttons'][MouseButton.Right.value] and self.rightEnabled:
                return True
            return False


class Watermark(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        if settings['GUI']['Watermark']['TopMost']:
            self.setWindowFlags(
                QtCore.Qt.WindowStaysOnTopHint |
                QtCore.Qt.FramelessWindowHint |
                QtCore.Qt.X11BypassWindowManagerHint |
                QtCore.Qt.ToolTip
            )
        else:
            self.setWindowFlags(
                QtCore.Qt.FramelessWindowHint |
                QtCore.Qt.X11BypassWindowManagerHint
            )
        self.setWindowOpacity(settings['GUI']['Watermark']['Opacity'])
        self.setStyleSheet(settings['GUI']['Watermark']['Style'])
        self.setGeometry(5, 5, 25, 25)
        self.label = QLabel(settings['GUI']['Watermark']['Text'], self)
        self.label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setStyleSheet(settings['GUI']['Watermark']['TextStyle'])
        self.layout = QGridLayout()
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)


class Enabled(QWidget):
    def __init__(self, i, button, doubleClicker):
        button = button.value
        self.button = button

        QWidget.__init__(self)
        if settings['GUI'][button]['TopMost']:
            self.setWindowFlags(
                QtCore.Qt.WindowStaysOnTopHint |
                QtCore.Qt.FramelessWindowHint |
                QtCore.Qt.X11BypassWindowManagerHint |
                QtCore.Qt.ToolTip
            )
        else:
            self.setWindowFlags(
                QtCore.Qt.FramelessWindowHint |
                QtCore.Qt.X11BypassWindowManagerHint
            )
        self.setWindowOpacity(settings['GUI'][button]['Opacity'])
        self.setStyleSheet(settings['GUI'][button]['Style'])
        self.setGeometry(5, i, 25, 25)
        self.label = QLabel(f"{button} - Disabled", self)
        self.label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setStyleSheet(settings['GUI'][button]['TextStyle'])
        self.layout = QGridLayout()
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)

        self.thread = threading.Thread(target=self.__updateLoop__)
        self.threadStarted = False
        self.doubleClicker = doubleClicker

    def __update__(self):
        self.label.setText(f"{self.button} - " + str(self.doubleClicker.isWhatEnabled(self.button)))

    def __updateLoop__(self):
        while True:
            self.__update__()
            time.sleep(0.001)

    def startThread(self):
        self.thread = threading.Thread(target=self.__updateLoop__)
        self.thread.start()
        self.threadStarted = True

    def stopThread(self):
        self.thread.join()
        self.threadStarted = False


def main():
    app = QApplication(sys.argv)

    doubleClicker = DoubleClicker()
    i = 50

    if settings['GUI']['Watermark']['Show']:
        watermark = Watermark()
        watermark.show()
    if settings['GUI'][MouseButton.Left.value]['Show'] and settings['Buttons'][MouseButton.Left.value]:
        leftEnabled = Enabled(i, MouseButton.Left, doubleClicker)
        leftEnabled.show()
        leftEnabled.startThread()
        i += 45
    if settings['GUI'][MouseButton.Right.value]['Show'] and settings['Buttons'][MouseButton.Right.value]:
        rightEnabled = Enabled(i, MouseButton.Right, doubleClicker)
        rightEnabled.show()
        rightEnabled.startThread()

    doubleClicker.startThread()

    app.exec_()


if __name__ == '__main__':
    main()
