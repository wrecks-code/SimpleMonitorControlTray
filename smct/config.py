import configparser
import os

import requests

from smct import paths, registry, ui

# config.ini structure
_ENCODING = "utf-8"

_SETTINGS_SECTION = "Settings"

_MONITOR_NAME_KEY = "monitor_name"
_MONITOR_SERIAL_KEY = "monitor_serial"
_MMT_PATH_KEY = "multimonitortool_executable"
_START_WITH_WINDOWS_KEY = "start_with_windows"
_FIRST_START_KEY = "first_start"

_configparser = configparser.ConfigParser()


def _check_for_missing_files():
    if not os.path.exists(paths.ASSETS_DIR_PATH):
        os.mkdir(paths.ASSETS_DIR_PATH)

    # Check for Icons
    # ! maybe send error message here?
    if not os.path.exists(paths.ASSETS_ICO_PATH):
        download_assets_file(os.path.basename(paths.ASSETS_ICO_PATH))
        # sys.exit(1)
    if not os.path.exists(paths.ASSETS_ICON_ENABLED_PATH):
        download_assets_file(os.path.basename(paths.ASSETS_ICON_ENABLED_PATH))
        # sys.exit(1)
    if not os.path.exists(paths.ASSETS_ICON_DISABLED_PATH):
        download_assets_file(os.path.basename(paths.ASSETS_ICON_DISABLED_PATH))
        # sys.exit(1)

    # Check for temp folder
    if not os.path.exists(paths.MMT_DIR_PATH):
        os.makedirs(paths.MMT_DIR_PATH)


def download_assets_file(image_name):
    image_url = paths.ASSETS_BASE_URL + image_name
    response = requests.get(image_url, stream=True, timeout=5)

    if response.status_code == 200:
        filename = response.url.split("/")[-1]

        with open(os.path.join(paths.ASSETS_DIR_PATH, filename), "wb") as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)


def init_config():
    if not os.path.exists(paths.CONFIG_PATH):
        _create_default_config_file()

    _check_for_missing_files()

    if get_start_with_windows_value():
        registry.add_to_autostart()
    else:
        registry.remove_from_autostart()

    if get_first_start_with_windows_value():
        ui.init_mmt_selection_frame()
        set_first_start_value(False)


def get_mmt_path_value():
    _read_from_config()
    return _configparser.get(_SETTINGS_SECTION, _MMT_PATH_KEY)


def set_mmt_path_value(_value):
    _configparser[_SETTINGS_SECTION][_MMT_PATH_KEY] = _value
    _write_to_config()


def get_monitor_name_value():
    _read_from_config()
    return _configparser.get(_SETTINGS_SECTION, _MONITOR_NAME_KEY)


def set_monitor_name_value(_value):
    _configparser[_SETTINGS_SECTION][_MONITOR_NAME_KEY] = _value
    _write_to_config()


def get_monitor_serial_value():
    _read_from_config()
    return _configparser.get(_SETTINGS_SECTION, _MONITOR_SERIAL_KEY)


def set_monitor_serial_value(_value):
    _configparser[_SETTINGS_SECTION][_MONITOR_SERIAL_KEY] = _value
    _write_to_config()


def get_start_with_windows_value():
    _read_from_config()
    return _configparser.getboolean(_SETTINGS_SECTION, _START_WITH_WINDOWS_KEY)


def set_start_with_windows_value(_value):
    value_str = "yes" if _value else "no"
    _configparser[_SETTINGS_SECTION][_START_WITH_WINDOWS_KEY] = value_str
    _write_to_config()


def get_first_start_with_windows_value():
    _read_from_config()
    return _configparser.getboolean(_SETTINGS_SECTION, _FIRST_START_KEY)


def set_first_start_value(_value):
    value_str = "yes" if _value else "no"
    _configparser[_SETTINGS_SECTION][_FIRST_START_KEY] = value_str
    _write_to_config()


def _read_from_config():
    _configparser.read(paths.CONFIG_PATH, encoding=_ENCODING)


def _write_to_config():
    with open(paths.CONFIG_PATH, "w", encoding=_ENCODING) as configfile:
        _configparser.write(configfile)


def _create_default_config_file():
    _configparser[_SETTINGS_SECTION] = {
        _MONITOR_NAME_KEY: "Example Monitor",
        _MONITOR_SERIAL_KEY: "12345",
        _MMT_PATH_KEY: "C:/MultiMonitorTool.exe",
        _START_WITH_WINDOWS_KEY: "no",
        _FIRST_START_KEY: "yes",
    }
    _write_to_config()
