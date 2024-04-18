import sys
import os
import shutil
import tkinter
import customtkinter
from customtkinter import filedialog
from smct import ui_strings, config, multimonitortool, paths

_ROOT_WINDOW = None
_SELECT_MMT_EXE_FRAME = None
_SELECT_MONITOR_FRAME = None


def init_root_window():
    # pylint: disable=global-statement
    global _ROOT_WINDOW, _SELECT_MMT_EXE_FRAME, _SELECT_MONITOR_FRAME

    customtkinter.set_ctk_parent_class(tkinter.Tk)

    customtkinter.set_appearance_mode(
        "dark"
    )  # Modes: "System" (standard), "Dark", "Light"
    customtkinter.set_default_color_theme(
        "dark-blue"
    )  # Themes: "blue" (standard), "green", "dark-blue"

    _ROOT_WINDOW = customtkinter.CTk()

    _ROOT_WINDOW.title(ui_strings.SHORT_NAME)
    _ROOT_WINDOW.resizable(False, False)

    _ROOT_WINDOW.geometry()
    _ROOT_WINDOW.protocol("WM_DELETE_WINDOW", exit_application)

    _SELECT_MMT_EXE_FRAME = customtkinter.CTkFrame(master=_ROOT_WINDOW)
    _SELECT_MONITOR_FRAME = customtkinter.CTkFrame(master=_ROOT_WINDOW)

    _init_mmt_selection_frame()


def exit_application():
    # clean up files if setup was interrupted
    shutil.rmtree(paths.MMT_DIR_PATH)
    shutil.rmtree(paths.ASSETS_DIR_PATH)
    os.remove(paths.CONFIG_PATH)
    _ROOT_WINDOW.destroy()
    sys.exit(1)


def _init_mmt_selection_frame():
    _ROOT_WINDOW.iconbitmap(paths.ASSETS_ICO_PATH)
    # _root_window.geometry("300x110")
    _SELECT_MMT_EXE_FRAME.pack(pady=10, padx=10, fill="both", expand=True)

    select_mmt_label = customtkinter.CTkLabel(
        text=ui_strings.SELECT_MMT_LABEL,
        master=_SELECT_MMT_EXE_FRAME,
        justify=customtkinter.CENTER,
    )
    select_mmt_label.pack(pady=5, padx=5)

    browse_button = customtkinter.CTkButton(
        text=ui_strings.BROWSE_BUTTON,
        master=_SELECT_MMT_EXE_FRAME,
        command=_browse_button_callback,
    )
    browse_button.pack(pady=10, padx=10)

    _ROOT_WINDOW.mainloop()


def _browse_button_callback():
    _exe_path = filedialog.askopenfilename(
        title=ui_strings.SELECT_MMT_LABEL,
        filetypes=[("MultiMonitorTool", "multimonitortool.exe")],
    )
    if not _exe_path:
        print(ui_strings.NO_FILE_SELECTED)
    else:
        config.set_mmt_path_value(_exe_path)
        _SELECT_MMT_EXE_FRAME.destroy()
        multimonitortool.enable_all_disabled_monitors()
        multimonitortool.save_mmt_config()
        _init_monitor_selection_frame()


def _init_monitor_selection_frame():
    # _root_window.geometry("300x160")
    _SELECT_MONITOR_FRAME.pack(pady=10, padx=10, fill="both", expand=True)

    _monitor_selection_label = customtkinter.CTkLabel(
        text=ui_strings.SELECT_MONITOR_LABEL,
        master=_SELECT_MONITOR_FRAME,
        justify=customtkinter.CENTER,
    )
    _monitor_selection_label.pack(pady=5, padx=5)

    monitor_selection_menu = customtkinter.CTkOptionMenu(
        _SELECT_MONITOR_FRAME,
        values=multimonitortool.get_monitor_selection_list(),
    )
    monitor_selection_menu.pack(pady=10, padx=10)

    def _select_monitor_button_callback():
        _menu_string = monitor_selection_menu.get().split("|")
        config.set_monitor_name_value(_menu_string[1].strip())
        config.set_monitor_serial_value(_menu_string[2].strip())

        _ROOT_WINDOW.destroy()

    _select_monitor_button = customtkinter.CTkButton(
        text=ui_strings.OK_BUTTON,
        master=_SELECT_MONITOR_FRAME,
        command=_select_monitor_button_callback,
    )
    _select_monitor_button.pack(pady=10, padx=10)
