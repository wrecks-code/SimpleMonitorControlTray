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
    monitor_df = _get_monitor_df()
    monitor_df["display_string"] = monitor_df.apply(
        lambda row: f"{row[MMT_CSV_NAME][-1]} | {row[MMT_CSV_MONITOR_NAME]} | {row[MMT_CSV_SERIAL_NUMBER]}",
        axis=1,
    )
    monitor_df["display_string"].apply(lambda x: log(f"Monitor detected: {x}"))
    return sorted(monitor_df["display_string"].tolist())


def _get_monitor_df():
    _run_mmt_command("/scomma", paths.MMT_CSV_PATH)
    return pd.read_csv(paths.MMT_CSV_PATH)


def _run_mmt_command(command, destination):
    command_line = [config.get_mmt_path_value(), command, destination]
    try:
        subprocess.run(command_line, check=True)
        log(f"{' '.join(command_line)}")
    except subprocess.CalledProcessError as error:
        log(f"{' '.join(command_line)} failed: {error}")


def save_mmt_config():
    _run_mmt_command("/SaveConfig", paths.MMT_CONFIG_PATH)


def enable_monitor():
    _run_mmt_command("/LoadConfig", paths.MMT_CONFIG_PATH)


def disable_monitor():
    if selected_monitor_id := get_selected_monitor_id():
        _run_mmt_command("/disable", selected_monitor_id)


def enable_all_disabled_monitors():
    disabled_monitor_ids = _get_all_disabled_monitor_ids()
    log("enable_all_disabled_monitors()")
    for _monitor_id in disabled_monitor_ids:
        _run_mmt_command("/enable", _monitor_id)


def get_selected_monitor_id():
    condition = (
        _get_monitor_df()[MMT_CSV_MONITOR_NAME] == config.get_monitor_name_value()
    ) & (
        _get_monitor_df()[MMT_CSV_SERIAL_NUMBER].astype(str)
        == config.get_monitor_serial_value()
    )
    filtered_df = _get_monitor_df().loc[condition]
    if not filtered_df.empty:
        return filtered_df.iloc[0][MMT_CSV_NAME][-1]


def _get_all_disabled_monitor_ids():
    monitor_df = _get_monitor_df()
    return (
        monitor_df[monitor_df[MMT_CSV_ACTIVE].str.lower() == MMT_CSV_NO][MMT_CSV_NAME]
        .apply(lambda x: x[-1])
        .tolist()
    )


def is_selected_monitor_enabled():
    df = _get_monitor_df()
    condition = (
        (df[MMT_CSV_MONITOR_NAME] == config.get_monitor_name_value())
        & (df[MMT_CSV_SERIAL_NUMBER].astype(str) == config.get_monitor_serial_value())
        & (df[MMT_CSV_ACTIVE].str.lower() == MMT_CSV_YES)
    )
    return condition.any()
