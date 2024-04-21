import configparser
import os
import requests
from smct import paths, ui
from smct.logger import log, INFO, ERROR

ENCODING = "utf-8"
_SECTION_SETTINGS = "Settings"
KEY_MONITOR_NAME = "monitor_name"
KEY_MONITOR_SERIAL = "monitor_serial"
KEY_MMT_PATH = "multimonitortool_executable"
KEY_START_WITH_WINDOWS = "start_with_windows"
KEY_FIRST_START = "first_start"

_DEFAULT_CONFIG = {
    KEY_MONITOR_NAME: "Example Monitor",
    KEY_MONITOR_SERIAL: "12345",
    KEY_MMT_PATH: "C:/MultiMonitorTool.exe",
    KEY_START_WITH_WINDOWS: "no",
    KEY_FIRST_START: "yes",
}
_SETTINGS_DICT: dict = {}


def _load_settings_into_memory():
    # pylint: disable=global-statement
    global _SETTINGS_DICT
    _config = configparser.ConfigParser()
    _config.read(paths.CONFIG_PATH)
    _SETTINGS_DICT = dict(_config.items(_SECTION_SETTINGS))


def _check_for_missing_files():
    def create_assets_dir():
        os.mkdir(paths.ASSETS_DIR_PATH)

    paths_actions = {
        paths.CONFIG_PATH: _create_default_config_file,
        paths.ASSETS_DIR_PATH: create_assets_dir,
        paths.ASSETS_ICO_PATH: lambda: download_assets_file(paths.ASSETS_ICO_NAME),
        paths.ASSETS_ICON_ENABLED_PATH: lambda: download_assets_file(
            paths.ASSETS_ICON_ENABLED_NAME
        ),
        paths.ASSETS_ICON_DISABLED_PATH: lambda: download_assets_file(
            paths.ASSETS_ICON_DISABLED_NAME
        ),
    }

    for path, action in paths_actions.items():
        if not os.path.exists(path):
            action()
            log(INFO, f"Creating or downloading {os.path.basename(path)}")


def download_assets_file(image_name: str):
    image_url = os.path.join(paths.ASSETS_BASE_URL, image_name)
    try:
        response = requests.get(image_url, stream=True, timeout=5)
        response.raise_for_status()
        with open(os.path.join(paths.ASSETS_DIR_PATH, image_name), "wb") as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)
    except requests.exceptions.RequestException as e:
        log(ERROR, f"Error occurred while downloading {image_name}: {e}")


def init_config():
    _check_for_missing_files()
    _load_settings_into_memory()
    if get_value(KEY_FIRST_START):
        # ui.init_root_window()
        setup_gui = ui.Application()
        setup_gui.root_window.mainloop()
        set_value(KEY_FIRST_START, False)


def get_value(_key: str) -> str | bool:
    if _SETTINGS_DICT[_key] == "yes":
        return True
    return False if _SETTINGS_DICT[_key] == "no" else _SETTINGS_DICT[_key]


def set_value(_key: str, _value: str | bool):
    if isinstance(_value, bool):
        _value = "yes" if _value is True else "no"

    log(INFO, f"{paths.CONFIG_FILE_NAME} - Setting {_key} to {_value}")
    config = configparser.ConfigParser()
    config.read(paths.CONFIG_PATH)
    config.set(_SECTION_SETTINGS, _key, _value)
    with open(paths.CONFIG_PATH, "w", encoding=ENCODING) as configfile:
        config.write(configfile)
    _load_settings_into_memory()


def _create_default_config_file():
    config = configparser.ConfigParser()
    config[_SECTION_SETTINGS] = _DEFAULT_CONFIG
    with open(paths.CONFIG_PATH, "w", encoding=ENCODING) as configfile:
        config.write(configfile)
