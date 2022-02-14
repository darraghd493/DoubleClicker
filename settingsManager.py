import os
import json

defaultSettings = {
    "Randomisation": {
        "BeforeClick": {
            "Min": 18,
            "Max": 27
        },
        "HoldClick": {
            "Min": 12,
            "Max": 17
        }
    },
    "Buttons": {
        "Left": True,
        "Right": False
    },
    "DoubleClicks": {
        "Min": 1,
        "Max": 2
    },
    "Keybinds": {
        "Left": "g",
        "Right": "x"
    },
    "GUI": {
        "Watermark": {
            "Show": True,
            "TopMost": True,
            "Opacity": 0.4,
            "Style": "background:rgba(0,0,0,0);opacity: 0;",
            "TextStyle": "color: rgb(225, 225, 225);font-size:18px;",
            "Text": "DoubleClicker"
        },
        "Left": {
            "Show": True,
            "TopMost": True,
            "Opacity": 0.4,
            "Style": "background:rgba(0,0,0,0);opacity: 0;",
            "TextStyle": "color: rgb(225, 225, 225);font-size:18px;",
            "Text": "DoubleClicker"
        },
        "Right": {
            "Show": True,
            "TopMost": True,
            "Opacity": 0.4,
            "Style": "background:rgba(0,0,0,0);opacity: 0;",
            "TextStyle": "color: rgb(225, 225, 225);font-size:18px;",
            "Text": "DoubleClicker"
        }
    }
}

settingsFolderPath = "C:/dogesupremacy/DoubleClicker/"
settingsFilePath = settingsFolderPath + "/settings.json"


def writeDefaultSettings():
    folders = settingsFolderPath.split("/")
    folders.pop(0)

    currentFolder = "C:/"
    for newFolder in folders:
        currentFolder += newFolder + "/"
        if not os.path.isdir(currentFolder):
            os.mkdir(currentFolder)

    if os.path.isfile(settingsFilePath):
        os.remove(settingsFilePath)
    with open(settingsFilePath, "w") as settingsFile:
        settingsFile.write(json.dumps(defaultSettings, indent=4))


def getSettings():
    if os.path.isdir(settingsFolderPath):
        try:
            with open(settingsFilePath, "r") as settingsFile:
                return json.loads(settingsFile.read())
        except FileNotFoundError:
            writeDefaultSettings()
            return defaultSettings
    else:
        writeDefaultSettings()
        return defaultSettings


settings = getSettings()


def getXOffset(num):
    return num + settings['Body']['X']


def getYOffset(num):
    return num + settings['Body']['X']
