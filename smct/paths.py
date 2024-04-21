import os
import sys

from smct import ui_strings


def get_base_path() -> str:
    if getattr(sys, "frozen", False):
        module_dir = os.path.dirname(sys.executable)
    else:
        module_dir = os.path.dirname(os.path.abspath(__file__))
    return strip_package_name_from_path(module_dir)


def strip_package_name_from_path(path) -> str:
    suffix = "smct"  # Removed the backslash for platform independence
    return path[: -len(suffix)] if path.endswith(suffix) else path


# NAMES
EXE_FILE_NAME = f"{ui_strings.APP_NAME}.exe"
CONFIG_FILE_NAME = "config.ini"
LOG_FILE_NAME = "smct.log"
ASSETS_DIR_NAME = "assets"

MMT_EXE_NAME = "MultiMonitorTool.exe"
MMT_CSV_NAME = "MultiMonitorToolScommaOutput.tmp"
MMT_CONFIG_NAME = "MultiMonitorToolConfig.ini"

ASSETS_ICON_ENABLED_NAME = "tray_monitor_enabled.png"
ASSETS_ICON_DISABLED_NAME = "tray_monitor_disabled.png"
ASSETS_ICO_NAME = "icon.ico"

# PATHS
ASSETS_BASE_URL = "https://raw.githubusercontent.com/wrecks-code/SimpleMonitorControlTray/main/assets/"

BASE_PATH = get_base_path()
EXE_PATH = os.path.join(BASE_PATH, EXE_FILE_NAME)

CONFIG_PATH = os.path.join(BASE_PATH, CONFIG_FILE_NAME)
LOG_PATH = os.path.join(BASE_PATH, LOG_FILE_NAME)
ASSETS_DIR_PATH = os.path.join(BASE_PATH, ASSETS_DIR_NAME)

MMT_CSV_PATH = os.path.join(BASE_PATH, MMT_CSV_NAME)
MMT_CONFIG_PATH = os.path.join(BASE_PATH, MMT_CONFIG_NAME)

ASSETS_ICON_ENABLED_PATH = os.path.join(ASSETS_DIR_PATH, ASSETS_ICON_ENABLED_NAME)
ASSETS_ICON_DISABLED_PATH = os.path.join(ASSETS_DIR_PATH, ASSETS_ICON_DISABLED_NAME)
ASSETS_ICO_PATH = os.path.join(ASSETS_DIR_PATH, ASSETS_ICO_NAME)
