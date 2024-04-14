import os
import shutil

import SimpleMonitorControlTrayModule.directoryHandler as dH

startup_folder = os.path.expanduser(
    "~\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup"
)
shortcut_filename = dH.APP_NAME + ".lnk"
shortcut_path = os.path.join(startup_folder, shortcut_filename)


def addShortcutToStartupFolder():
    shutil.copy2(dH.getDirectory(), shortcut_path)


def removeShortcutFromStartupFolder():
    if is_shortcut_in_startup():
        os.remove(shortcut_path)


def is_shortcut_in_startup():
    return os.path.exists(shortcut_path)
