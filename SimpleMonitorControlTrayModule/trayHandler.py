import os

import pystray
from PIL import Image
from pystray import MenuItem as item

import SimpleMonitorControlTrayModule.configHandler as cH
import SimpleMonitorControlTrayModule.directoryHandler as dH
import SimpleMonitorControlTrayModule.multiMonitorToolHandler as mH
import SimpleMonitorControlTrayModule.registryHandler as rH

icon = None
itemTitle = ""

imageIconEnabled = Image.open(cH.asset_iconEnabled_path)
imageIconDisabled = Image.open(cH.asset_iconDisabled_path)


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
    os.startfile(cH.config_file_path)


def toggleAutostart(icon):
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

    new_menu = (
        item(itemTitle, toggleAutostart),
        pystray.Menu.SEPARATOR,
        item(
            "Save current monitor layout",
            saveMultiMonitorToolConfigClicked,
        ),
        item("Open Config.ini", openConfigClicked),
        pystray.Menu.SEPARATOR,
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
        pystray.Menu.SEPARATOR,
        item(
            "Save current monitor layout",
            saveMultiMonitorToolConfigClicked,
        ),
        item("Open Config.ini", openConfigClicked),
        pystray.Menu.SEPARATOR,
        item("Exit", exitItemClicked),
    )

    firstImageIcon = None

    mH.updateMonitorsCSV()

    if mH.isMonitorEnabled():
        firstImageIcon = imageIconEnabled
        if not os.path.exists(cH.mmt_config_path):
            mH.saveMultiMonitorToolConfig()
    else:
        firstImageIcon = imageIconDisabled

    icon = pystray.Icon(dH.APP_NAME, firstImageIcon, dH.APP_NAME, menu)
    icon.run()
