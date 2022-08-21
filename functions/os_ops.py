import os
import subprocess as sp

paths = {
    'pycharm': "C:\\Users\\Tony\\AppData\\Local\\JetBrains\\Toolbox\\apps\\PyCharm-P\\ch-0\\222.3345.131\\bin\\pycharm64.exe",
    'discord': "C:\\Users\\Tony\\AppData\\Local\\Discord\\Update.exe --processStart Discord.exe",
    'calculator': "C:\\Windows\\System32\\calc.exe",
    'steam': "C:\\Program Files (x86)\\Steam\\steam.exe"
}


def open_camera():
    sp.run('start microsoft.windows.camera', shell=True)


def open_pycharm():
    os.startfile(paths['pycharm'])


def open_discord():
    os.startfile(paths['discord'])


def open_calculator():
    sp.Popen(paths['calculator'])


def open_steam():
    os.startfile(paths['steam'])


def open_cmd():
    os.system('start cmd')
