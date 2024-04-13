import os

import pystray
from PIL import Image
from pystray import MenuItem as item

import SimpleMonitorControlTray.configHandler as cH
import SimpleMonitorControlTray.monitorHandler as mH

script_dir = os.getcwd()

imageIconEnabled = Image.open(os.path.join(script_dir, "assets\iconEnabled.png"))
imageIconDisabled = Image.open(os.path.join(script_dir, "assets\iconDisabled.png"))

title = "SimpleMonitorControlTray"

icon = None


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


def quitItemClicked():
    icon.stop()


def openConfigClicked():
    os.startfile(os.path.join(script_dir, cH.config_file_path))


checked = False


def toggleAutostart(icon):
    # Recreate the menu with the updated title for "Autostart"
    new_menu = (
        item("New Title", toggleAutostart),
        item(
            "Save current monitor layout (used when enabling)",
            saveMultiMonitorToolConfigClicked,
        ),
        item("Open Config.ini", openConfigClicked),
        item("Quit", quitItemClicked),
    )
    icon.menu = new_menu


def initTray():
    global icon
    menu = (
        item(title, iconTrayClicked, default=True, visible=False),
        item("Autostart", toggleAutostart),
        item(
            "Save current monitor layout (used when enabling)",
            saveMultiMonitorToolConfigClicked,
        ),
        item("Open Config.ini", openConfigClicked),
        item("Quit", quitItemClicked),
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
