import os

import pystray
from PIL import Image
from pystray import MenuItem as item

from smct_pkg import config, multimonitortool, paths, registry, ui_strings

ICON = None

ICON_ENABLED_IMAGE = None
ICON_DISABLED_IMAGE = None


def save_mmt_config_clicked():
    multimonitortool.save_mmt_config()


def icon_tray_clicked():
    if multimonitortool.is_monitor_enabled():
        multimonitortool.disable_monitor()
        ICON.icon = ICON_DISABLED_IMAGE
    else:
        multimonitortool.enable_monitor()
        ICON.icon = ICON_ENABLED_IMAGE


def exit_clicked():
    ICON.stop()


def open_folder_clicked():
    os.startfile(paths.BASE_PATH)


def startup_with_windows_clicked(icon):
    config.START_WITH_WINDOWS_VALUE = not config.START_WITH_WINDOWS_VALUE
    config.set_config_value(
        config.SETTINGS_SECTION,
        config.START_WITH_WINDOWS_KEY,
        config.START_WITH_WINDOWS_VALUE,
    )
    if config.START_WITH_WINDOWS_VALUE:
        registry.add_to_autostart()
    else:
        registry.remove_from_autostart()

    new_menu = (
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
    icon.menu = new_menu


def init_tray():
    # pylint: disable=global-statement
    global ICON_ENABLED_IMAGE, ICON_DISABLED_IMAGE
    ICON_ENABLED_IMAGE = Image.open(paths.ASSETS_ICON_ENABLED_PATH)
    ICON_DISABLED_IMAGE = Image.open(paths.ASSETS_ICON_DISABLED_PATH)

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

    if multimonitortool.is_monitor_enabled():
        first_image_icon = ICON_ENABLED_IMAGE
        multimonitortool.save_mmt_config()
    else:
        first_image_icon = ICON_DISABLED_IMAGE

    # pylint: disable=global-statement
    global ICON
    ICON = pystray.Icon(
        ui_strings.APP_NAME, first_image_icon, ui_strings.APP_NAME, menu
    )
    ICON.run()
