import configparser
import os

import SimpleMonitorControlTrayModule.directoryHandler as dH
import SimpleMonitorControlTrayModule.multiMonitorToolHandler as mH
import SimpleMonitorControlTrayModule.notificationHandler as nH

base_path = dH.getDirectory()
config_file_path = base_path + r"\config.ini"
assets_folder_path = base_path + r"\assets"
temp_folder_path = base_path + r"\temp"

mmt_csv_export_path = temp_folder_path + r"\MultiMonitorToolOutput.csv"
mmt_config_path = temp_folder_path + r"\MultiMonitorToolConfig"
asset_iconEnabled_path = assets_folder_path + r"\iconEnabled.png"
asset_iconDisabled_path = assets_folder_path + r"\iconDisabled.png"

fileNotFoundString = " file not found. Exiting."

# TODO: change MONITOR_NAME to actual name or id
MULTIMONITORTOOL_PATH, MONITOR_NAME, AUTOSTART, FIRST_START = (
    "",
    "",
    False,
    True,
)


def check_for_missing_files():
    # Check for assets folder
    if not os.path.exists(assets_folder_path):
        os.makedirs(assets_folder_path)
    # Check for IconEnabled
    if not os.path.exists(asset_iconEnabled_path):
        nH.sendError(asset_iconEnabled_path + fileNotFoundString)

    # Check for IconDisabled
    if not os.path.exists(asset_iconDisabled_path):
        nH.sendError(asset_iconDisabled_path + fileNotFoundString)

    # Check for MultiMonitorTool
    if not os.path.exists(MULTIMONITORTOOL_PATH):
        nH.sendError(MULTIMONITORTOOL_PATH + fileNotFoundString)

    # Check for temp folder
    if not os.path.exists(temp_folder_path):
        os.makedirs(temp_folder_path)

    # Check for MultiMonitorTool CSV
    if not os.path.exists(mmt_csv_export_path):
        mH.saveMultiMonitorToolConfig()


def read_config():
    # Check if config.ini file is present
    if not os.path.exists(config_file_path):
        nH.sendError(config_file_path + fileNotFoundString)

    global AUTOSTART, MULTIMONITORTOOL_PATH, MONITOR_NAME, FIRST_START

    config = configparser.ConfigParser()

    config.read(config_file_path, encoding="utf-8")

    MULTIMONITORTOOL_PATH = config.get("SETTINGS", "multimonitorpath")
    MONITOR_NAME = config.get("SETTINGS", "monitor_name")
    AUTOSTART = config.get("SETTINGS", "autostart")
    FIRST_START = config.get("SETTINGS", "first_start")

    check_for_missing_files()

    if FIRST_START == "True":
        nH.sendNotification(
            "If you do not have all Monitors enabled and configured as you like right now, please do so and then right click the tray icon to save the monitor layout.",
            30,
        )
        FIRST_START = "False"
        set_config_value("SETTINGS", "first_start", FIRST_START)


def set_config_value(category, key, value):
    config = configparser.ConfigParser()
    config.read(config_file_path, encoding="utf-8")
    config[category][key] = value
    with open(config_file_path, "w") as configfile:
        config.write(configfile)
    # print("Setting config value: " + key + " to " + value)


def get_config_value(category, key):
    config = configparser.ConfigParser()
    config.read(config_file_path, encoding="utf-8")
    return config.get(category, key)
