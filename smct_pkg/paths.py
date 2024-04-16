import os
import sys

from smct_pkg import ui_strings as ui_strings


def get_base_path():
    if getattr(sys, "frozen", False):
        module_dir = os.path.dirname(sys.executable)
    else:
        module_dir = os.path.dirname(os.path.abspath(__file__))
    return strip_package_name_from_path(module_dir)


def strip_package_name_from_path(path):
    suffix = "\\smct_pkg"
    if path.endswith(suffix):
        return path[: -len(suffix)]
    else:
        return path


# PATHS
BASE_PATH = get_base_path()
EXE_PATH = BASE_PATH + "\\" + ui_strings.APP_NAME + ".exe"

# os.path.join(paths.BASE_PATH, keyName + ".exe")
CONFIG_PATH = BASE_PATH + r"\config.ini"
ASSETS_DIR_PATH = BASE_PATH + r"\assets"
TEMP_DIR_PATH = BASE_PATH + r"\temp"

MMT_CSV_PATH = TEMP_DIR_PATH + r"\MultiMonitorToolOutput.csv"
MMT_CONFIG_PATH = TEMP_DIR_PATH + r"\MultiMonitorToolConfig"
ASSETS_ICON_ENABLED_PATH = ASSETS_DIR_PATH + r"\iconEnabled.png"
ASSETS_ICON_DISABLED_PATH = ASSETS_DIR_PATH + r"\iconDisabled.png"
