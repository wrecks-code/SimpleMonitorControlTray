import csv
import subprocess

import smct_pkg.config as config
import smct_pkg.paths as paths


def save_mmt_config():
    subprocess.run(
        [
            paths.MULTIMONITORTOOL_PATH,
            "/SaveConfig",
            paths.MMT_CONFIG_PATH,
        ]
    )


def update_mmt_csv():
    # Run MultiMonitorTool.exe with the /scomma option to save the monitors list into a CSV file
    subprocess.run(
        [
            config.MMT_PATH,
            "/scomma",
            paths.MMT_CSV_PATH,
        ]
    )


def enable_monitor():
    subprocess.run(
        [
            config.MMT_PATH,
            "/LoadConfig",
            paths.MMT_CONFIG_PATH,
        ]
    )


def disable_monitor():
    # Run MultiMonitorTool.exe with the /disable option to disable the third monitor
    subprocess.run(
        [
            config.MMT_PATH,
            "/disable",
            get_monitor_id(),
        ]
    )


def get_monitor_id():
    with open(paths.MMT_CSV_PATH, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                if row["Monitor Name"] == config.MONITOR_NAME:
                    monitor_id = row["Name"]
                    return monitor_id[-1]
            except KeyError:
                pass


def is_monitor_enabled():
    with open(paths.MMT_CSV_PATH, "r") as file:
        reader = csv.DictReader(file)

        for row in reader:
            try:
                monitor_name = row["Monitor Name"]
                monitor_active = row["Active"]
                if (
                    monitor_name == config.MONITOR_NAME
                    and monitor_active.upper() == "YES"
                ):
                    return True
            except KeyError:
                pass
    return False
