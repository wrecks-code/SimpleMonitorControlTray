import csv
import subprocess

import SimpleMonitorControlTrayModule.configHandler as cH


def saveMultiMonitorToolConfig():
    subprocess.run(
        [
            cH.MULTIMONITORTOOL_PATH,
            "/SaveConfig",
            cH.mmt_config_path,
        ]
    )


def updateMonitorsCSV():
    # Run MultiMonitorTool.exe with the /scomma option to save the monitors list into a CSV file
    subprocess.run(
        [
            cH.MULTIMONITORTOOL_PATH,
            "/scomma",
            cH.mmt_csv_export_path,
        ]
    )


def enableMonitor():
    subprocess.run(
        [
            cH.MULTIMONITORTOOL_PATH,
            "/LoadConfig",
            cH.mmt_config_path,
        ]
    )


def disableMonitor():
    # Run MultiMonitorTool.exe with the /disable option to disable the third monitor
    subprocess.run(
        [
            cH.MULTIMONITORTOOL_PATH,
            "/disable",
            cH.MONITOR_NAME[-1],
        ]
    )


def isMonitorEnabled():
    # Check if the third monitor is listed in the CSV file
    with open(cH.mmt_csv_export_path, "r") as file:
        reader = csv.DictReader(file)

        for row in reader:
            try:
                monitor_name = row["Name"]
                monitor_active = row["Active"]
                if monitor_name == cH.MONITOR_NAME and monitor_active.upper() == "YES":
                    return True
            except KeyError:
                pass  # Ignore rows with missing keys
    return False  # No match found
