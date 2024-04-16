import winreg

import smct_pkg.paths as paths
import smct_pkg.ui_strings as ui_strings

keyName = ui_strings.APP_NAME
registry_key = r"Software\Microsoft\Windows\CurrentVersion\Run"


def is_autostartkey_in_registry():
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, registry_key)
        value, _ = winreg.QueryValueEx(key, keyName)
        winreg.CloseKey(key)
        return True
    except FileNotFoundError:
        return False


def add_to_autostart():
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, registry_key, 0, winreg.KEY_WRITE)
    winreg.SetValueEx(
        key,
        keyName,
        0,
        winreg.REG_SZ,
        f'"{paths.EXE_PATH[0].upper() + paths.EXE_PATH[1:]}"',
    )
    winreg.CloseKey(key)


def remove_from_autostart():
    try:
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER, registry_key, 0, winreg.KEY_ALL_ACCESS
        )
        winreg.DeleteValue(key, keyName)
        winreg.CloseKey(key)
    except:
        pass
