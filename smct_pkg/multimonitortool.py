import csv
import subprocess

from smct_pkg import config, paths


def _run_mmt_command(command, destination):
    try:
        subprocess.run(
            [
                config.MMT_PATH_VALUE,
                command,
                destination,
            ],
            check=True,
        )
    except subprocess.CalledProcessError as error:
        print(f"MultiMonitorTool.exe {command} failed: {error}")


def save_mmt_config():
    _run_mmt_command("/SaveConfig", paths.MMT_CONFIG_PATH)


def update_mmt_csv():
    _run_mmt_command("/scomma", paths.MMT_CSV_PATH)


def enable_monitor():
    _run_mmt_command("/LoadConfig", paths.MMT_CONFIG_PATH)


def disable_monitor():
    _run_mmt_command("/disable", get_monitor_id())


# TODO Encoding Issue?


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


"""
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
    return False"""
