import configparser
import os

import SimpleMonitorControlTrayModule.directoryHandler as dH
import SimpleMonitorControlTrayModule.monitorHandler as mH
import SimpleMonitorControlTrayModule.notificationHandler as nH
import SimpleMonitorControlTrayModule.trayHandler as tH

config_file_path = "config.ini"
assets_folder = "assets"
asset_iconEnabled = "assets\iconEnabled.png"
asset_iconDisabled = "assets\iconDisabled.png"

fileNotFound = " file not found. Exiting."

MULTIMONITORTOOL_PATH, CSV_FILE_PATH, MM_CONFIG_FILE_PATH, MONITOR_NAME, AUTOSTART = (
    None,
    None,
    None,
    None,
    False,
)


def check_for_missing_files():

    if not os.path.exists(MULTIMONITORTOOL_PATH):
        nH.sendError(MULTIMONITORTOOL_PATH + fileNotFound)
        tH.exitItemClicked()
    if not os.path.exists(os.path.join(dH.getDirectory(), asset_iconEnabled)):
        nH.sendError(asset_iconDisabled + fileNotFound)
        tH.exitItemClicked()

    if not os.path.exists(CSV_FILE_PATH):
        mH.saveMultiMonitorToolConfig()

    multiMonitorToolOutputPath = os.path.join(dH.getDirectory(), "MultiMonitorTool")

    if not os.path.exists(multiMonitorToolOutputPath):
        os.makedirs(multiMonitorToolOutputPath)

    # TODO add assets folder check

    nH.sendNotification(
        "If you do not have all Monitors enabled and configured as you like right now, please do so and then right click the tray icon and save the configuration",
        20,
    )


def read_config():

    global AUTOSTART, MULTIMONITORTOOL_PATH, CSV_FILE_PATH, MM_CONFIG_FILE_PATH, MONITOR_NAME

    if not os.path.exists(os.path.join(dH.getDirectory(), asset_iconEnabled)):
        nH.sendError(config_file_path + fileNotFound)
        tH.exitItemClicked()

    config = configparser.ConfigParser()

    config.read(config_file_path, encoding="utf-8")

    MULTIMONITORTOOL_PATH = config.get("SETTINGS", "multimonitorpath")
    MONITOR_NAME = config.get("SETTINGS", "monitor_name")
    AUTOSTART = config.get("SETTINGS", "autostart")
    CSV_FILE_PATH = config.get("DEV", "mm_csv_export_path")
    MM_CONFIG_FILE_PATH = config.get("DEV", "mm_config_file_path")

    check_for_missing_files()


def set_config_value(category, key, value):
    config = configparser.ConfigParser()
    config.read(config_file_path, encoding="utf-8")
    config[category][key] = value
    with open(config_file_path, "w") as configfile:
        config.write(configfile)
    print("Setting config value: " + key + " to " + value)


def get_config_value(category, key):
    config = configparser.ConfigParser()
    config.read(config_file_path, encoding="utf-8")
    return config.get(category, key)
