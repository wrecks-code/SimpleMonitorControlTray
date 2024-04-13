import os
import winreg as reg

keyName = "SimpleMonitorControlTray"

exe_path = os.path.join(os.getcwd(), keyName + ".exe")
registry_key = r"Software\Microsoft\Windows\CurrentVersion\Run"


def add_to_autostart():
    key = reg.OpenKey(reg.HKEY_CURRENT_USER, registry_key, 0, reg.KEY_WRITE)
    reg.SetValueEx(key, keyName, 0, reg.REG_SZ, exe_path)
    reg.CloseKey(key)


def remove_from_autostart():
    key = reg.OpenKey(reg.HKEY_CURRENT_USER, registry_key, 0, reg.KEY_ALL_ACCESS)
    reg.DeleteValue(key, keyName)
    reg.CloseKey(key)
