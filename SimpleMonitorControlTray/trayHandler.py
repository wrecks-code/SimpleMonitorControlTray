import os

import pystray
from PIL import Image
from pystray import MenuItem as item

import main
import SimpleMonitorControlTray.configHandler as cH
import SimpleMonitorControlTray.monitorHandler as mH
import SimpleMonitorControlTray.registryHandler as rH

# TODO this returns the wrong path (System32) if run from registry autostart
script_dir = main.script_dir

imageIconEnabled = Image.open(os.path.join(script_dir, "assets\iconEnabled.png"))
imageIconDisabled = Image.open(os.path.join(script_dir, "assets\iconDisabled.png"))

title = "SimpleMonitorControlTray"

icon = None
itemTitle = ""


def saveMultiMonitorToolConfigClicked():
    mH.saveMultiMonitorToolConfig()


def iconTrayClicked():
    mH.updateMonitorsCSV()
    if mH.isMonitorEnabled():
        mH.disableMonitor()
        icon.icon = imageIconDisabled
    else:
        mH.enableMonitor()
        icon.icon = imageIconEnabled


def exitItemClicked():
    icon.stop()


def openConfigClicked():
    os.startfile(os.path.join(script_dir, cH.config_file_path))


def toggleAutostartInConfig():
    global itemTitle
    if cH.AUTOSTART == "False":
        itemTitle = "Disable Autostart"
        rH.add_to_autostart()
        cH.set_config_value("SETTINGS", "autostart", "True")
        cH.AUTOSTART = "True"
    else:
        itemTitle = "Enable Autostart"
        rH.remove_from_autostart()
        cH.set_config_value("SETTINGS", "autostart", "False")
        cH.AUTOSTART = "False"


def toggleAutostart(icon):
    toggleAutostartInConfig()
    new_menu = (
        item(itemTitle, toggleAutostart),
        item(
            "Save current monitor layout (used when enabling)",
            saveMultiMonitorToolConfigClicked,
        ),
        item("Open Config.ini", openConfigClicked),
        item("Exit", exitItemClicked),
    )
    icon.menu = new_menu


def initTray():
    global icon
    if cH.AUTOSTART == "True":
        itemTitle = "Disable Autostart"
    else:
        itemTitle = "Enable Autostart"

    menu = (
        item(title, iconTrayClicked, default=True, visible=False),
        item(itemTitle, toggleAutostart),
        item(
            "Save current monitor layout (used when enabling)",
            saveMultiMonitorToolConfigClicked,
        ),
        item("Open Config.ini", openConfigClicked),
        item("Exit", exitItemClicked),
    )

    firstImageIcon = None

    mH.updateMonitorsCSV()

    if mH.isMonitorEnabled():
        firstImageIcon = imageIconEnabled
        if not os.path.exists(cH.MM_CONFIG_FILE_PATH):
            mH.saveMultiMonitorToolConfig()
    else:
        firstImageIcon = imageIconDisabled

    icon = pystray.Icon(title, firstImageIcon, title, menu)
    icon.run()
