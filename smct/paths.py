import os
import sys

from smct import ui_strings


def get_base_path():
    if getattr(sys, "frozen", False):
        module_dir = os.path.dirname(sys.executable)
    else:
        module_dir = os.path.dirname(os.path.abspath(__file__))
    return strip_package_name_from_path(module_dir)


def strip_package_name_from_path(path):
    suffix = "\\smct"
    if path.endswith(suffix):
        return path[: -len(suffix)]
    else:
        return path


# PATHS
BASE_PATH = get_base_path()
EXE_PATH = BASE_PATH + "\\" + ui_strings.APP_NAME + ".exe"

CONFIG_PATH = BASE_PATH + "\\config.ini"
LOG_PATH = BASE_PATH + "\\smct.log"
ASSETS_DIR_PATH = BASE_PATH + "\\assets"
MMT_DIR_PATH = BASE_PATH + "\\mmt"

MMT_CSV_PATH = MMT_DIR_PATH + "\\MultiMonitorToolOutput.csv"
MMT_CONFIG_PATH = MMT_DIR_PATH + "\\MultiMonitorToolConfig"

ASSETS_ICON_ENABLED_PATH = ASSETS_DIR_PATH + "\\iconEnabled.png"
ASSETS_ICON_DISABLED_PATH = ASSETS_DIR_PATH + "\\iconDisabled.png"
ASSETS_ICO_PATH = ASSETS_DIR_PATH + "\\icon.ico"

ASSETS_BASE_URL = "https://raw.githubusercontent.com/wrecks-code/SimpleMonitorControlTray/main/assets/"
