import winreg
from smct import paths, ui_strings

KEY_NAME = ui_strings.APP_NAME
REGISTRY_KEY = r"Software\Microsoft\Windows\CurrentVersion\Run"


def is_autostartkey_in_registry():
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, REGISTRY_KEY, 0, winreg.KEY_READ)
        value = winreg.QueryValueEx(key, KEY_NAME)
        winreg.CloseKey(key)
        return value is not None
    except FileNotFoundError:
        return False


def add_to_autostart():
    try:
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER, REGISTRY_KEY, 0, winreg.KEY_WRITE
        )
        exe_path = paths.EXE_PATH[0].upper() + paths.EXE_PATH[1:]
        winreg.SetValueEx(key, KEY_NAME, 0, winreg.REG_SZ, exe_path)
        winreg.CloseKey(key)
    except PermissionError:
        # print(f"Error occurred while adding to autostart: {e}")
        pass


def remove_from_autostart():
    try:
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER, REGISTRY_KEY, 0, winreg.KEY_ALL_ACCESS
        )
        winreg.DeleteValue(key, KEY_NAME)
        winreg.CloseKey(key)
    except (FileNotFoundError, PermissionError):
        # print(f"Error occurred while removing from autostart: {e}")
        pass
