import SimpleMonitorControlTrayModule.configHandler as cH
import SimpleMonitorControlTrayModule.trayHandler as tH


def main():
    cH.read_config()
    tH.initTray()


if __name__ == "__main__":
    main()
