import subprocess

import pandas as pd
from smct import config, paths


def _get_monitor_df():
    _run_mmt_command("/scomma", paths.MMT_CSV_PATH)
    _monitor_df = []

    data = pd.read_csv(paths.MMT_CSV_PATH)
    for index in range(len(data)):
        _monitor_df.append(data.iloc[index])
    return _monitor_df


def get_monitor_selection_list():
    _monitor_selection_list = []
    for _monitor in _get_monitor_df():
        _monitor_name = _monitor["Monitor Name"]
        _monitor_serial = _monitor["Monitor Serial Number"]
        _monitor_selection_list.append(f"{_monitor_name} | {_monitor_serial}")
    return _monitor_selection_list


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
        print(f"{config.MMT_PATH_VALUE} {command} {destination} failed: {error}")


def save_mmt_config():
    _run_mmt_command("/SaveConfig", paths.MMT_CONFIG_PATH)


def enable_monitor():
    _run_mmt_command("/LoadConfig", paths.MMT_CONFIG_PATH)


def disable_monitor():
    _run_mmt_command("/disable", get_selected_monitor_id())


def enable_all_disabled_monitors():
    for _monitor_id in _get_all_disabled_monitor_ids():
        _run_mmt_command("/enable", _monitor_id)


def get_selected_monitor_id():
    for monitor in _get_monitor_df():
        if (
            monitor["Monitor Name"] == config.MONITOR_NAME_VALUE
            and str(monitor["Monitor Serial Number"]) == config.MONITOR_SERIAL_VALUE
        ):
            _id = monitor["Name"]
            return _id[-1]


def _get_all_disabled_monitor_ids():
    _monitor_id_list = []
    for monitor in _get_monitor_df():
        if monitor["Active"].upper() == "NO":
            _id = monitor["Name"]
            _monitor_id_list.append(_id[-1])
    return _monitor_id_list


def is_selected_monitor_enabled():
    for monitor in _get_monitor_df():
        if (
            monitor["Monitor Name"] == config.MONITOR_NAME_VALUE
            and str(monitor["Monitor Serial Number"]) == config.MONITOR_SERIAL_VALUE
            and monitor["Active"].upper() == "YES"
        ):
            return True
    return False
