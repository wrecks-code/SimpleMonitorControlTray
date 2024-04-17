import configparser
import os
import sys

from smct_pkg import (
    notification,
    paths,
    registry,
    ui,
    ui_strings,
)

ENCODING = "utf-8"

# keys
SETTINGS_SECTION = "Settings"
MONITOR_NAME_KEY = "monitor_name"
MONITOR_SERIAL_KEY = "monitor_serial"
MMT_PATH_KEY = "multimonitortool_executable"
START_WITH_WINDOWS_KEY = "start_with_windows"
FIRT_START_KEY = "first_start"

# values
MMT_PATH_VALUE = ""
MONITOR_NAME_VALUE = ""
MONITOR_SERIAL_VALUE = ""
START_WITH_WINDOWS_VALUE = False
FIRST_START_VALUE = True

_configparser = configparser.ConfigParser()


def check_for_missing_files():
    # Check for Icons
    if not os.path.exists(paths.ASSETS_ICON_ENABLED_PATH):
        notification.send_error(
            paths.ASSETS_ICON_ENABLED_PATH + ui_strings.FILE_NOT_FOUND
        )
        sys.exit(1)
    if not os.path.exists(paths.ASSETS_ICON_DISABLED_PATH):
        notification.send_error(
            paths.ASSETS_ICON_DISABLED_PATH + ui_strings.FILE_NOT_FOUND
        )
        sys.exit(1)

    # Check for temp folder
    if not os.path.exists(paths.TEMP_DIR_PATH):
        os.makedirs(paths.TEMP_DIR_PATH)


def read_config():
    # Check if config.ini file is present
    if not os.path.exists(paths.CONFIG_PATH):
        _create_default_config_file()

    _configparser.read(paths.CONFIG_PATH, encoding=ENCODING)

    # * pylint: disable=global-statement
    global START_WITH_WINDOWS_VALUE, MMT_PATH_VALUE, MONITOR_NAME_VALUE, MONITOR_SERIAL_VALUE, FIRST_START_VALUE

    MMT_PATH_VALUE = _configparser.get(SETTINGS_SECTION, MMT_PATH_KEY)
    MONITOR_NAME_VALUE = _configparser.get(SETTINGS_SECTION, MONITOR_NAME_KEY)
    MONITOR_SERIAL_VALUE = _configparser.get(SETTINGS_SECTION, MONITOR_SERIAL_KEY)
    START_WITH_WINDOWS_VALUE = _configparser.getboolean(
        SETTINGS_SECTION, START_WITH_WINDOWS_KEY
    )
    FIRST_START_VALUE = _configparser.getboolean(SETTINGS_SECTION, FIRT_START_KEY)

    check_for_missing_files()

    if START_WITH_WINDOWS_VALUE:
        registry.add_to_autostart()
    else:
        registry.remove_from_autostart()

    if FIRST_START_VALUE:
        ui.init_mmt_selection_frame()
        FIRST_START_VALUE = False
        set_config_value(SETTINGS_SECTION, FIRT_START_KEY, FIRST_START_VALUE)


def _create_default_config_file():
    _configparser["Settings"] = {
        MONITOR_NAME_KEY: "Example Monitor",
        MONITOR_SERIAL_KEY: "12345",
        MMT_PATH_KEY: "C:/MultiMonitorTool.exe",
        START_WITH_WINDOWS_KEY: "no",
        FIRT_START_KEY: "yes",
    }
    with open(paths.CONFIG_PATH, "w", encoding=ENCODING) as _file_object:
        _configparser.write(_file_object)


def set_config_value(section, key, value):
    if isinstance(value, bool):
        value_str = "yes" if value else "no"
    else:
        value_str = str(value)
    _configparser[section][key] = value_str
    with open(paths.CONFIG_PATH, "w", encoding=ENCODING) as configfile:
        _configparser.write(configfile)
    # print("Setting config value: " + key + " to " + value)


def get_config_value(section, key):
    return _configparser.get(section, key)
