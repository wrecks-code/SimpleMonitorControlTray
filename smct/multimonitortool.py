import subprocess
import pandas as pd
from smct import config, paths
from smct.logger import log

MMT_CSV_MONITOR_NAME = "Monitor Name"
MMT_CSV_SERIAL_NUMBER = "Monitor Serial Number"
MMT_CSV_NAME = "Name"
MMT_CSV_ACTIVE = "Active"
MMT_CSV_YES = "yes"
MMT_CSV_NO = "no"


def get_monitor_selection_list():
    _monitor_selection_list = []
    monitor_df = _get_monitor_df()
    # pylint: disable=unused-variable
    for index, row in monitor_df.iterrows():
        _monitor_id = row[MMT_CSV_NAME][-1]
        _monitor_name = row[MMT_CSV_MONITOR_NAME]
        _monitor_serial = row[MMT_CSV_SERIAL_NUMBER]
        _monitor_selection_list.append(
            f"{_monitor_id} | {_monitor_name} | {_monitor_serial}"
        )
        log(f"Monitor detected: {_monitor_id} | {_monitor_name} | {_monitor_serial}")
        _monitor_selection_list.sort()
    return _monitor_selection_list


def _get_monitor_df():
    _run_mmt_command("/scomma", paths.MMT_CSV_PATH)
    data = pd.read_csv(paths.MMT_CSV_PATH)
    return data


def _run_mmt_command(command, destination):
    try:
        subprocess.run(
            [
                config.get_mmt_path_value(),
                command,
                destination,
            ],
            check=True,
        )
        log(f"MultiMonitorTool.exe {command} {destination}")
    except subprocess.CalledProcessError as error:
        log(f"MultiMonitorTool.exe {command} {destination} failed: {error}")


def save_mmt_config():
    _run_mmt_command("/SaveConfig", paths.MMT_CONFIG_PATH)


def enable_monitor():
    _run_mmt_command("/LoadConfig", paths.MMT_CONFIG_PATH)


def disable_monitor():
    selected_monitor_id = get_selected_monitor_id()
    if selected_monitor_id:
        _run_mmt_command("/disable", selected_monitor_id)


def enable_all_disabled_monitors():
    disabled_monitor_ids = _get_all_disabled_monitor_ids()
    for _monitor_id in disabled_monitor_ids:
        _run_mmt_command("/enable", _monitor_id)


def get_selected_monitor_id():
    # pylint: disable=unused-variable
    for index, monitor in _get_monitor_df().iterrows():
        if (
            monitor[MMT_CSV_MONITOR_NAME] == config.get_monitor_name_value()
            and str(monitor[MMT_CSV_SERIAL_NUMBER]) == config.get_monitor_serial_value()
        ):
            return monitor[MMT_CSV_NAME][-1]


def _get_all_disabled_monitor_ids():
    monitor_df = _get_monitor_df()
    disabled_monitor_ids = []
    # pylint: disable=unused-variable
    for index, monitor in monitor_df.iterrows():
        if monitor[MMT_CSV_ACTIVE].lower() == MMT_CSV_NO:
            disabled_monitor_ids.append(monitor[MMT_CSV_NAME][-1])
    return disabled_monitor_ids


def is_selected_monitor_enabled():
    # pylint: disable=unused-variable
    for index, monitor in _get_monitor_df().iterrows():
        if (
            monitor[MMT_CSV_MONITOR_NAME] == config.get_monitor_name_value()
            and str(monitor[MMT_CSV_SERIAL_NUMBER]) == config.get_monitor_serial_value()
            and monitor[MMT_CSV_ACTIVE].lower() == MMT_CSV_YES
        ):
            return True
    return False
