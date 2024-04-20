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
_configparser = configparser.ConfigParser()


def _check_for_missing_files():
    paths_actions = {
        paths.CONFIG_PATH: _create_default_config_file,
        paths.ASSETS_DIR_PATH: lambda: os.mkdir(paths.ASSETS_DIR_PATH),
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


def download_assets_file(image_name):
    image_url = os.path.join(paths.ASSETS_BASE_URL, image_name)
    response = requests.get(image_url, stream=True, timeout=5)
    if response.status_code == 200:
        with open(os.path.join(paths.ASSETS_DIR_PATH, image_name), "wb") as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)
    else:
        log(
            ERROR,
            f"Error occurred while downloading {image_name}: {response.status_code}",
        )


def init_config():
    _check_for_missing_files()
    if get_value(KEY_FIRST_START):
        ui.init_root_window()
        set_value(KEY_FIRST_START, False)


def get_value(key):
    _read_from_config()
    value = _configparser.get(_SECTION_SETTINGS, key)
    return value.lower() == "yes" if value.lower() in ["yes", "no"] else value


def set_value(key, value):
    if isinstance(value, bool):
        value_str = "yes" if value else "no"
    else:
        value_str = str(value)

    log(INFO, f"{paths.CONFIG_FILE_NAME} - Setting {key} to {value_str}")
    _configparser[_SECTION_SETTINGS][key] = value_str
    _write_to_config()


def _read_from_config():
    _configparser.read(paths.CONFIG_PATH, encoding=ENCODING)


def _write_to_config():
    with open(paths.CONFIG_PATH, "w", encoding=ENCODING) as configfile:
        _configparser.write(configfile)


def _create_default_config_file():
    _configparser[_SECTION_SETTINGS] = _DEFAULT_CONFIG
    _write_to_config()
