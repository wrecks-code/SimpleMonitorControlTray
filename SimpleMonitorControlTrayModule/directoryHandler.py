import os
import sys

APP_NAME = "SimpleMonitorControlTray"


def getDirectory():
    if getattr(sys, "frozen", False):
        module_dir = os.path.dirname(sys.executable)
    else:
        module_dir = os.path.dirname(os.path.abspath(__file__))
    return stripPath(module_dir)


def stripPath(path):
    suffix = "\\SimpleMonitorControlTrayModule"
    if path.endswith(suffix):
        return path[: -len(suffix)]
    else:
        return path
