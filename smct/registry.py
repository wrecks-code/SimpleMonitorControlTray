import winreg
from smct import paths, ui_strings
from smct.logger import log, ERROR

KEY_NAME = ui_strings.APP_NAME
REGISTRY_KEY = r"Software\Microsoft\Windows\CurrentVersion\Run"


def handle_registry_errors(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (FileNotFoundError, PermissionError) as e:
            if func.__name__ != "is_autostartkey_in_registry":
                log(ERROR, f"Failed to modify autostart: {e} in {REGISTRY_KEY}")

    return wrapper


class RegistryKey:
    def __init__(self, access):
        self.access = access
        self.key = None

    def __enter__(self):
        self.key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER, REGISTRY_KEY, 0, self.access
        )
        return self.key

    def __exit__(self, exc_type, exc_val, exc_tb):
        winreg.CloseKey(self.key)


@handle_registry_errors
def is_autostartkey_in_registry():
    with RegistryKey(winreg.KEY_READ) as key:
        value = winreg.QueryValueEx(key, KEY_NAME)
        exe_path = f"{paths.EXE_PATH[0].upper()}{paths.EXE_PATH[1:]}"
        return value[0] == exe_path


@handle_registry_errors
def add_to_autostart():
    with RegistryKey(winreg.KEY_WRITE) as key:
        exe_path = f"{paths.EXE_PATH[0].upper()}{paths.EXE_PATH[1:]}"
        winreg.SetValueEx(key, KEY_NAME, 0, winreg.REG_SZ, exe_path)


@handle_registry_errors
def remove_from_autostart():
    with RegistryKey(winreg.KEY_ALL_ACCESS) as key:
        winreg.DeleteValue(key, KEY_NAME)
