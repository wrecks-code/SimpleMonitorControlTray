import os

import pystray
from PIL import Image
from pystray import MenuItem as item

from smct_pkg import config, multimonitortool, paths, registry, ui_strings

ICON = None

icon_enabled_image = Image.open(paths.ASSETS_ICON_ENABLED_PATH)
icon_disabled_image = Image.open(paths.ASSETS_ICON_DISABLED_PATH)


def save_mmt_config_clicked():
    multimonitortool.save_mmt_config()


def icon_tray_clicked():
    if multimonitortool.is_monitor_enabled():
        multimonitortool.disable_monitor()
        ICON.icon = icon_disabled_image
    else:
        multimonitortool.enable_monitor()
        ICON.icon = icon_enabled_image


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
        first_image_icon = icon_enabled_image
        if not os.path.exists(paths.MMT_CONFIG_PATH):
            multimonitortool.save_mmt_config()
    else:
        first_image_icon = icon_disabled_image

    # pylint: disable=global-statement
    global ICON
    ICON = pystray.Icon(
        ui_strings.APP_NAME, first_image_icon, ui_strings.APP_NAME, menu
    )
    ICON.run()
