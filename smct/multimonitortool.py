import subprocess
import os
import pandas as pd
from smct import config, paths
from smct.logger import log, INFO, ERROR

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
    monitor_df["display_string"].apply(lambda x: log(INFO, f"Monitor detected: {x}"))
    return sorted(monitor_df["display_string"].tolist())


def _get_monitor_df():
    _run_mmt_command("/scomma", paths.MMT_CSV_PATH)
    _return_df = pd.read_csv(paths.MMT_CSV_PATH)
    os.remove(paths.MMT_CSV_PATH)
    return _return_df


def _run_mmt_command(command, destination):
    command_line = [config.get_value(config.KEY_MMT_PATH), command, destination]
    try:
        subprocess.run(command_line, check=True)
        log(INFO, f"{paths.MMT_EXE_NAME} {command} {os.path.basename(destination)}")
    except subprocess.CalledProcessError as error:
        log(ERROR, f"{paths.MMT_EXE_NAME} {command} failed: {error}")


def save_mmt_config():
    _run_mmt_command("/SaveConfig", paths.MMT_CONFIG_PATH)


def enable_monitor():
    _run_mmt_command("/LoadConfig", paths.MMT_CONFIG_PATH)


def disable_monitor(monitor_id):
    _run_mmt_command("/disable", str(monitor_id))


# returns if selected monitor is enabled AND its id
def get_state_and_id_of_monitor():
    df = _get_monitor_df()
    id_condition = (
        df[MMT_CSV_MONITOR_NAME] == config.get_value(config.KEY_MONITOR_NAME)
    ) & (
        df[MMT_CSV_SERIAL_NUMBER].astype(str)
        == config.get_value(config.KEY_MONITOR_SERIAL)
    )
    state_condition = id_condition & (df[MMT_CSV_ACTIVE].str.lower() == MMT_CSV_YES)
    return (
        len(df.loc[state_condition]) == 1,
        df.loc[id_condition].iloc[0][MMT_CSV_NAME][-1],
    )
