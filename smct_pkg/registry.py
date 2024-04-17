import winreg

from smct_pkg import paths, ui_strings

KEY_NAME = ui_strings.APP_NAME
REGISTRY_KEY = r"Software\Microsoft\Windows\CurrentVersion\Run"


def is_autostartkey_in_registry():
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, REGISTRY_KEY)
        _ = winreg.QueryValueEx(key, KEY_NAME)
        winreg.CloseKey(key)
        return True
    except FileNotFoundError:
        return False


def add_to_autostart():
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, REGISTRY_KEY, 0, winreg.KEY_WRITE)
    winreg.SetValueEx(
        key,
        KEY_NAME,
        0,
        winreg.REG_SZ,
        f'"{paths.EXE_PATH[0].upper() + paths.EXE_PATH[1:]}"',
    )
    winreg.CloseKey(key)


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
