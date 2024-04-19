import os

import pystray
from PIL import Image
from pystray import MenuItem as item

from smct import config, multimonitortool, paths, registry, ui_strings
from smct.logger import log

ICON = None


def save_mmt_config_clicked():
    multimonitortool.save_mmt_config()


def icon_tray_clicked():
    log("icon_tray_clicked()")
    if multimonitortool.is_selected_monitor_enabled():
        multimonitortool.disable_monitor()
        ICON.icon = get_icon_image(False)
    else:
        multimonitortool.enable_monitor()
        ICON.icon = get_icon_image(True)


def exit_clicked():
    ICON.stop()


def open_folder_clicked():
    os.startfile(paths.BASE_PATH)


def startup_with_windows_clicked():
    _current_start_with_windows_value = config.get_start_with_windows_value()
    config.set_start_with_windows_value(not _current_start_with_windows_value)

    if config.get_start_with_windows_value():
        registry.add_to_autostart()
    else:
        registry.remove_from_autostart()


def get_icon_image(_option):
    if _option:
        return Image.open(paths.ASSETS_ICON_ENABLED_PATH)
    return Image.open(paths.ASSETS_ICON_DISABLED_PATH)


def init_tray():
    menu = (
        item(ui_strings.APP_NAME, icon_tray_clicked, default=True, visible=False),
        item(
            ui_strings.STARTUP_WITH_WINDOWS,
            startup_with_windows_clicked,
            checked=lambda icon: registry.is_autostartkey_in_registry(),
        ),
        pystray.Menu.SEPARATOR,
        item(
            ui_strings.SAVE_MONITOR_LAYOUT,
            save_mmt_config_clicked,
        ),
        item(ui_strings.OPEN_FOLDER, open_folder_clicked),
        pystray.Menu.SEPARATOR,
        item(ui_strings.EXIT, exit_clicked),
    )

    first_image_icon = None

    if multimonitortool.is_selected_monitor_enabled():
        first_image_icon = get_icon_image(True)
        multimonitortool.save_mmt_config()
    else:
        first_image_icon = get_icon_image(False)

    # pylint: disable=global-statement
    global ICON
    ICON = pystray.Icon(
        ui_strings.APP_NAME, first_image_icon, ui_strings.APP_NAME, menu
    )
    ICON.run()
