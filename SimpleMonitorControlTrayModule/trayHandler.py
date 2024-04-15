import os

import pystray
from PIL import Image
from pystray import MenuItem as item

import SimpleMonitorControlTrayModule.configHandler as cH
import SimpleMonitorControlTrayModule.directoryHandler as dH
import SimpleMonitorControlTrayModule.multiMonitorToolHandler as mH
import SimpleMonitorControlTrayModule.registryHandler as rH

icon = None

imageIconEnabled = Image.open(cH.asset_iconEnabled_path)
imageIconDisabled = Image.open(cH.asset_iconDisabled_path)

# Strings
startupWithWindowsString = "Startup with Windows"
saveCurrentMonitorLayoutString = "Save current monitor layout"
openFolderString = "Open Folder"
exitString = "Exit"

configKeysSettingsString = "SETTINGS"
configKeysAutostartString = "autostart"


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


def openFolderClicked():
    os.startfile(dH.getDirectory())


def toggleAutostart(icon):
    if cH.AUTOSTART == "False":
        rH.add_to_autostart()
        cH.set_config_value(configKeysSettingsString, configKeysAutostartString, "True")
        cH.AUTOSTART = "True"
    else:
        rH.remove_from_autostart()
        cH.set_config_value(
            configKeysSettingsString, configKeysAutostartString, "False"
        )
        cH.AUTOSTART = "False"

    new_menu = (
        item(
            startupWithWindowsString,
            toggleAutostart,
            checked=lambda icon: rH.isAutostartKeyinRegistry(),
        ),
        pystray.Menu.SEPARATOR,
        item(
            saveCurrentMonitorLayoutString,
            saveMultiMonitorToolConfigClicked,
        ),
        item(openFolderString, openFolderClicked),
        pystray.Menu.SEPARATOR,
        item(exitString, exitItemClicked),
    )
    icon.menu = new_menu


def initTray():
    global icon

    menu = (
        item(dH.APP_NAME, iconTrayClicked, default=True, visible=False),
        item(
            startupWithWindowsString,
            toggleAutostart,
            checked=lambda icon: rH.isAutostartKeyinRegistry(),
        ),
        pystray.Menu.SEPARATOR,
        item(
            saveCurrentMonitorLayoutString,
            saveMultiMonitorToolConfigClicked,
        ),
        item(openFolderString, openFolderClicked),
        pystray.Menu.SEPARATOR,
        item(exitString, exitItemClicked),
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
