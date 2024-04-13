import SimpleMonitorControlTray.configHandler as cH
import SimpleMonitorControlTray.trayHandler as tH


def main():
    cH.read_config()
    tH.initTray()


if __name__ == "__main__":
    main()
