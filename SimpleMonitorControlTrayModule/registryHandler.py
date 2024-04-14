import os
import winreg as reg

keyName = "SimpleMonitorControlTray"

import SimpleMonitorControlTrayModule.directoryHandler as dH

exe_path = os.path.join(dH.getDirectory(), keyName + ".exe")
registry_key = r"Software\Microsoft\Windows\CurrentVersion\Run"


def isAutostartKeyinRegistry():
    try:
        key = reg.OpenKey(reg.HKEY_CURRENT_USER, registry_key)
        value, _ = reg.QueryValueEx(key, keyName)
        reg.CloseKey(key)
        return True
    except FileNotFoundError:
        return False


def add_to_autostart():
    key = reg.OpenKey(reg.HKEY_CURRENT_USER, registry_key, 0, reg.KEY_WRITE)
    reg.SetValueEx(
        key, keyName, 0, reg.REG_SZ, f'"{exe_path[0].upper() + exe_path[1:]}"'
    )
    reg.CloseKey(key)


def remove_from_autostart():
    try:
        key = reg.OpenKey(reg.HKEY_CURRENT_USER, registry_key, 0, reg.KEY_ALL_ACCESS)
        reg.DeleteValue(key, keyName)
        reg.CloseKey(key)
    except:
        pass
