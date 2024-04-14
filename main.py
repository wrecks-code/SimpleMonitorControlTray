import os
import sys

import SimpleMonitorControlTray.configHandler as cH
import SimpleMonitorControlTray.trayHandler as tH

script_dir = ""

if getattr(sys, "frozen", False):
    script_dir = os.path.dirname(sys.executable)
else:
    script_dir = os.path.dirname(os.path.abspath(__file__))


def main():
    cH.read_config()
    tH.initTray()


if __name__ == "__main__":
    main()
