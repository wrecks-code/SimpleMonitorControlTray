import configparser
import os

import smct_pkg.mmt as mmt
import smct_pkg.notification as notification
import smct_pkg.paths as paths

MMT_PATH, MONITOR_NAME, AUTOSTART, FIRST_START = (
    "",
    "",
    False,
    True,
)


def check_for_missing_files():
    # Check for assets folder
    if not os.path.exists(paths.ASSETS_DIR_PATH):
        os.makedirs(paths.ASSETS_DIR_PATH)
    # Check for Icons
    if not os.path.exists(paths.ASSETS_ICON_ENABLED_PATH):
        notification.send_error(paths.ASSETS_ICON_ENABLED_PATH + paths.FILE_NOT_FOUND)
    if not os.path.exists(paths.ASSETS_ICON_DISABLED_PATH):
        notification.send_error(paths.ASSETS_ICON_DISABLED_PATH + paths.FILE_NOT_FOUND)

    # Check for MultiMonitorTool
    if not os.path.exists(MMT_PATH):
        notification.send_error(MMT_PATH + paths.FILE_NOT_FOUND)

    # Check for temp folder
    if not os.path.exists(paths.TEMP_DIR_PATH):
        os.makedirs(paths.TEMP_DIR_PATH)

    # Check for MultiMonitorTool CSV
    if not os.path.exists(paths.MMT_CSV_PATH):
        mmt.save_mmt_config()


def read_config():
    # Check if config.ini file is present
    if not os.path.exists(paths.CONFIG_PATH):
        notification.send_error(paths.CONFIG_PATH + paths.FILE_NOT_FOUND)

    global AUTOSTART, MMT_PATH, MONITOR_NAME, FIRST_START

    config = configparser.ConfigParser()

    config.read(paths.CONFIG_PATH, encoding="utf-8")

    MMT_PATH = config.get("SETTINGS", "multimonitorpath")
    MONITOR_NAME = config.get("SETTINGS", "monitor_name")
    AUTOSTART = config.get("SETTINGS", "autostart")
    FIRST_START = config.get("SETTINGS", "first_start")

    check_for_missing_files()

    if FIRST_START == "True":
        notification.send_notification(
            "If you do not have all Monitors enabled and configured as you like right now, please do so and then right click the tray icon to save the monitor layout.",
            30,
        )
        FIRST_START = "False"
        set_config_value("SETTINGS", "first_start", FIRST_START)


def set_config_value(category, key, value):
    config = configparser.ConfigParser()
    config.read(paths.CONFIG_PATH, encoding="utf-8")
    config[category][key] = value
    with open(paths.CONFIG_PATH, "w") as configfile:
        config.write(configfile)
    # print("Setting config value: " + key + " to " + value)


def get_config_value(category, key):
    config = configparser.ConfigParser()
    config.read(paths.CONFIG_PATH, encoding="utf-8")
    return config.get(category, key)
