import winreg
from smct import paths, ui_strings
from smct.logger import log

KEY_NAME = ui_strings.APP_NAME
REGISTRY_KEY = r"Software\Microsoft\Windows\CurrentVersion\Run"


class RegistryKey:
    # Automatically called when an object is created.
    def __init__(self, sub_key, access):
        self.sub_key = sub_key
        self.access = access
        self.key = None

    # Automatically called when entering a context manager (e.g., using the with statement).
    def __enter__(self):
        self.key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER, self.sub_key, 0, self.access
        )
        return self.key

    # Automatically called when exiting a context manager.
    def __exit__(self, exc_type, exc_val, exc_tb):
        winreg.CloseKey(self.key)


def is_autostartkey_in_registry():
    try:
        with RegistryKey(REGISTRY_KEY, winreg.KEY_READ) as key:
            value = winreg.QueryValueEx(key, KEY_NAME)
            return value is not None
    except FileNotFoundError:
        return False


def add_to_autostart():
    try:
        with RegistryKey(REGISTRY_KEY, winreg.KEY_WRITE) as key:
            exe_path = paths.EXE_PATH[0].upper() + paths.EXE_PATH[1:]
            winreg.SetValueEx(key, KEY_NAME, 0, winreg.REG_SZ, exe_path)
            log(f"Enabled autostart, wrote {KEY_NAME} to {REGISTRY_KEY}")
    except PermissionError as e:
        log(f"Failed to enable autostart: {e} in {REGISTRY_KEY}")


def remove_from_autostart():
    try:
        with RegistryKey(REGISTRY_KEY, winreg.KEY_ALL_ACCESS) as key:
            winreg.DeleteValue(key, KEY_NAME)
            log(f"Disabled autostart, removed {KEY_NAME} from {REGISTRY_KEY}")
    except (FileNotFoundError, PermissionError) as e:
        log(f"Failed to disable autostart: {e} in {REGISTRY_KEY}")
