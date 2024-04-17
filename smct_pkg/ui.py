import sys
import os
import shutil
import tkinter
import customtkinter
from customtkinter import filedialog
from smct_pkg import ui_strings, config, multimonitortool, paths

customtkinter.set_ctk_parent_class(tkinter.Tk)

customtkinter.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme(
    "dark-blue"
)  # Themes: "blue" (standard), "green", "dark-blue"

_root_window = customtkinter.CTk()

_root_window.title(ui_strings.SHORT_NAME)
_root_window.resizable(False, False)

_root_window.geometry()

_select_mmt_exe_frame = customtkinter.CTkFrame(master=_root_window)
_select_monitor_frame = customtkinter.CTkFrame(master=_root_window)


def exit_application():
    # clean up files if setup was interrupted
    shutil.rmtree(paths.TEMP_DIR_PATH)
    os.remove(paths.CONFIG_PATH)
    _root_window.destroy()
    sys.exit(1)


_root_window.protocol("WM_DELETE_WINDOW", exit_application)


def init_mmt_selection_frame():
    _root_window.iconbitmap(paths.ASSETS_ICO_PATH)
    # _root_window.geometry("300x110")
    _select_mmt_exe_frame.pack(pady=10, padx=10, fill="both", expand=True)

    select_mmt_label = customtkinter.CTkLabel(
        text=ui_strings.SELECT_MMT_LABEL,
        master=_select_mmt_exe_frame,
        justify=customtkinter.CENTER,
    )
    select_mmt_label.pack(pady=5, padx=5)

    browse_button = customtkinter.CTkButton(
        text=ui_strings.BROWSE_BUTTON,
        master=_select_mmt_exe_frame,
        command=_browse_button_callback,
    )
    browse_button.pack(pady=10, padx=10)

    _root_window.mainloop()


def _browse_button_callback():
    _exe_path = filedialog.askopenfilename(
        title=ui_strings.SELECT_MMT_LABEL,
        filetypes=[("MultiMonitorTool", "multimonitortool.exe")],
    )
    if not _exe_path:
        print(ui_strings.NO_FILE_SELECTED)
    else:
        config.MMT_PATH_VALUE = _exe_path
        config.set_config_value(
            config.SETTINGS_SECTION,
            config.MMT_PATH_KEY,
            config.MMT_PATH_VALUE,
        )
        _select_mmt_exe_frame.destroy()
        _init_monitor_selection_frame()


def _init_monitor_selection_frame():
    # _root_window.geometry("300x160")
    _select_monitor_frame.pack(pady=10, padx=10, fill="both", expand=True)

    _monitor_selection_label = customtkinter.CTkLabel(
        text=ui_strings.SELECT_MONITOR_LABEL,
        master=_select_monitor_frame,
        justify=customtkinter.CENTER,
    )
    _monitor_selection_label.pack(pady=5, padx=5)

    monitor_selection_menu = customtkinter.CTkOptionMenu(
        _select_monitor_frame,
        values=multimonitortool.get_monitor_selection_list(),
    )
    monitor_selection_menu.pack(pady=10, padx=10)

    def _select_monitor_button_callback():
        _menu_string = monitor_selection_menu.get().split("|")

        config.MONITOR_NAME_VALUE = _menu_string[0].strip()
        config.set_config_value(
            config.SETTINGS_SECTION,
            config.MONITOR_NAME_KEY,
            config.MONITOR_NAME_VALUE,
        )

        config.MONITOR_SERIAL_VALUE = _menu_string[1].strip()
        config.set_config_value(
            config.SETTINGS_SECTION,
            config.MONITOR_SERIAL_KEY,
            config.MONITOR_SERIAL_VALUE,
        )
        _root_window.destroy()

    _select_monitor_button = customtkinter.CTkButton(
        text=ui_strings.OK_BUTTON,
        master=_select_monitor_frame,
        command=_select_monitor_button_callback,
    )
    _select_monitor_button.pack(pady=10, padx=10)
