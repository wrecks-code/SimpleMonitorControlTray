import SimpleMonitorControlTrayModule.configHandler as cH
import SimpleMonitorControlTrayModule.trayHandler as tH

"""pyinstaller --noconfirm --onefile --windowed --icon "C:/Users/Wreck/Documents/Github/SimpleMonitorControlTray/assets/iconEnabled.ico"  "C:/Users/Wreck/Documents/Github/SimpleMonitorControlTray/main.py"""


def main():
    cH.read_config()
    tH.initTray()


if __name__ == "__main__":
    main()
