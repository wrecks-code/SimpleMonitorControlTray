import csv
import subprocess

import SimpleMonitorControlTrayModule.configHandler as ch


def saveMultiMonitorToolConfig():
    subprocess.run(
        [
            ch.MULTIMONITORTOOL_PATH,
            "/SaveConfig",
            ch.MM_CONFIG_FILE_PATH,
        ]
    )


def updateMonitorsCSV():
    # Run MultiMonitorTool.exe with the /scomma option to save the monitors list into a CSV file
    subprocess.run(
        [
            ch.MULTIMONITORTOOL_PATH,
            "/scomma",
            ch.CSV_FILE_PATH,
        ]
    )


def enableMonitor():
    subprocess.run(
        [
            ch.MULTIMONITORTOOL_PATH,
            "/LoadConfig",
            ch.MM_CONFIG_FILE_PATH,
        ]
    )


def disableMonitor():
    # Run MultiMonitorTool.exe with the /disable option to disable the third monitor
    subprocess.run(
        [
            ch.MULTIMONITORTOOL_PATH,
            "/disable",
            ch.MONITOR_NAME[-1],
        ]
    )


def isMonitorEnabled():
    # Check if the third monitor is listed in the CSV file
    with open(ch.CSV_FILE_PATH, "r") as file:
        reader = csv.DictReader(file)

        for row in reader:
            try:
                monitor_name = row["Name"]
                monitor_active = row["Active"]
                if monitor_name == ch.MONITOR_NAME and monitor_active.upper() == "YES":
                    return True
            except KeyError:
                pass  # Ignore rows with missing keys
    return False  # No match found
