import configparser
import os

import SimpleMonitorControlTray.monitorHandler as mH
import SimpleMonitorControlTray.notificationHandler as nH
import SimpleMonitorControlTray.trayHandler as tH

currentPath = os.getcwd()
config_file_path = "config.ini"
assets_folder = "assets"
asset_iconEnabled = "assets\iconEnabled.png"
asset_iconDisabled = "assets\iconDisabled.png"

fileNotFound = " file not found. Exiting."

MULTIMONITORTOOL_PATH, CSV_FILE_PATH, MM_CONFIG_FILE_PATH, MONITOR_NAME = (
    None,
    None,
    None,
    None,
)


def check_for_missing_files():

    if not os.path.exists(MULTIMONITORTOOL_PATH):
        nH.sendError(MULTIMONITORTOOL_PATH + fileNotFound)
        tH.quitItemClicked()
    if not os.path.exists(os.path.join(currentPath, asset_iconEnabled)):
        nH.sendError(asset_iconDisabled + fileNotFound)
        tH.quitItemClicked()

    if not os.path.exists(CSV_FILE_PATH):
        mH.saveMultiMonitorToolConfig()

    multiMonitorToolOutputPath = os.path.join(currentPath, "MultiMonitorTool")

    if not os.path.exists(multiMonitorToolOutputPath):
        os.makedirs(multiMonitorToolOutputPath)

    nH.sendNotification(
        "If you do not have all Monitors enabled and configured as you like right now, please do so and then right click the tray icon and save the configuration",
        20,
    )


def read_config():

    global MULTIMONITORTOOL_PATH, CSV_FILE_PATH, MM_CONFIG_FILE_PATH, MONITOR_NAME

    if not os.path.exists(config_file_path):
        nH.sendError(config_file_path + fileNotFound)
        tH.quitItemClicked()

    config = configparser.ConfigParser()

    config.read(config_file_path, encoding="utf-8")

    MULTIMONITORTOOL_PATH = config.get("SETTINGS", "multimonitorpath")
    MONITOR_NAME = config.get("SETTINGS", "monitor_name")
    CSV_FILE_PATH = config.get("DEV", "mm_csv_export_path")
    MM_CONFIG_FILE_PATH = config.get("DEV", "mm_config_file_path")

    check_for_missing_files()
