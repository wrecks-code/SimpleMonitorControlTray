import os

import pystray
from PIL import Image
from pystray import MenuItem as item

import smct_pkg.config as config
import smct_pkg.mmt as mmt
import smct_pkg.paths as paths
import smct_pkg.registry as registry
import smct_pkg.ui_strings as ui_strings

icon = None

icon_enabled_image = Image.open(paths.ASSETS_ICON_ENABLED_PATH)
icon_disabled_image = Image.open(paths.ASSETS_ICON_DISABLED_PATH)


def save_mmt_config_clicked():
    mmt.save_mmt_config()


def icon_tray_clicked():
    mmt.update_mmt_csv()
    if mmt.is_monitor_enabled():
        mmt.disable_monitor()
        icon.icon = icon_disabled_image
    else:
        mmt.enable_monitor()
        icon.icon = icon_enabled_image


def exit_clicked():
    icon.stop()


def open_folder_clicked():
    os.startfile(paths.BASE_PATH)


def toggle_autostart(icon):
    if config.AUTOSTART == "False":
        registry.add_to_autostart()
        config.set_config_value("SETTINGS", "autostart", "True")
        config.AUTOSTART = "True"
    else:
        registry.remove_from_autostart()
        config.set_config_value("SETTINGS", "autostart", "False")
        config.AUTOSTART = "False"

    new_menu = (
        item(
            ui_strings.STARTUP_WITH_WINDOWS,
            toggle_autostart,
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
    global icon

    menu = (
        item(ui_strings.APP_NAME, icon_tray_clicked, default=True, visible=False),
        item(
            ui_strings.STARTUP_WITH_WINDOWS,
            toggle_autostart,
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

    firstImageIcon = None

    mmt.update_mmt_csv()

    if mmt.is_monitor_enabled():
        firstImageIcon = icon_enabled_image
        if not os.path.exists(paths.MMT_CONFIG_PATH):
            mmt.save_mmt_config()
    else:
        firstImageIcon = icon_disabled_image

    icon = pystray.Icon(ui_strings.APP_NAME, firstImageIcon, ui_strings.APP_NAME, menu)
    icon.run()
