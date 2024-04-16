import csv
import subprocess

from smct_pkg import config, paths


def save_mmt_config():
    try:
        subprocess.run(
            [
                config.MMT_PATH_VALUE,
                "/SaveConfig",
                paths.MMT_CONFIG_PATH,
            ],
            check=True,
        )
    except subprocess.CalledProcessError as error:
        print(f"MultiMonitorTool.exe /SaveConfig failed: {error}")


def update_mmt_csv():
    # Run MultiMonitorTool.exe with the /scomma option to save the monitors list into a CSV file
    try:
        subprocess.run(
            [
                config.MMT_PATH_VALUE,
                "/scomma",
                paths.MMT_CSV_PATH,
            ],
            check=True,
        )
    except subprocess.CalledProcessError as error:
        print(f"MultiMonitorTool.exe /scomma failed: {error}")


def enable_monitor():
    try:
        subprocess.run(
            [
                config.MMT_PATH_VALUE,
                "/LoadConfig",
                paths.MMT_CONFIG_PATH,
            ],
            check=True,
        )
    except subprocess.CalledProcessError as error:
        print(f"MultiMonitorTool.exe /LoadConfig failed: {error}")


def disable_monitor():
    try:
        subprocess.run(
            [
                config.MMT_PATH_VALUE,
                "/disable",
                get_monitor_id(),
            ],
            check=True,
        )
    except subprocess.CalledProcessError as error:
        print(f"MultiMonitorTool.exe /LoadConfig failed: {error}")


def get_monitor_id():
    with open(paths.MMT_CSV_PATH, "r", encoding=config.ENCODING) as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                if row["Monitor Name"] == config.MONITOR_NAME_VALUE:
                    monitor_id = row["Name"]
                    return monitor_id[-1]
            except KeyError:
                pass
    return 0


def is_monitor_enabled():
    with open(paths.MMT_CSV_PATH, "r", encoding=config.ENCODING) as file:
        reader = csv.DictReader(file)

        for row in reader:
            try:
                monitor_name = row["Monitor Name"]
                monitor_active = row["Active"]
                if (
                    monitor_name == config.MONITOR_NAME_VALUE
                    and monitor_active.upper() == "YES"
                ):
                    return True
            except KeyError:
                pass
    return False
