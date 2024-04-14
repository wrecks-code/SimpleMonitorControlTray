import os

import pystray
from PIL import Image
from pystray import MenuItem as item

import SimpleMonitorControlTrayModule.autoStartHandler as aH
import SimpleMonitorControlTrayModule.configHandler as cH
import SimpleMonitorControlTrayModule.directoryHandler as dH
import SimpleMonitorControlTrayModule.monitorHandler as mH

icon = None
itemTitle = ""

script_dir = dH.getDirectory()
assets_dir = script_dir + "\\assets"

imageIconEnabled = Image.open(os.path.join(assets_dir, "iconEnabled.png"))
imageIconDisabled = Image.open(os.path.join(assets_dir, "iconDisabled.png"))


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


def toggleAutostart(icon):
    global itemTitle
    if cH.AUTOSTART == "False":
        itemTitle = "Disable Autostart"
        aH.addShortcutToStartupFolder()
        cH.set_config_value("SETTINGS", "autostart", "True")
        cH.AUTOSTART = "True"
    else:
        itemTitle = "Enable Autostart"
        aH.removeShortcutFromStartupFolder()
        cH.set_config_value("SETTINGS", "autostart", "False")
        cH.AUTOSTART = "False"

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
        item(dH.APP_NAME, iconTrayClicked, default=True, visible=False),
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

    icon = pystray.Icon(dH.APP_NAME, firstImageIcon, dH.APP_NAME, menu)
    icon.run()
