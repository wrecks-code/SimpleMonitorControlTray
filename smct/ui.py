import sys
import os
import shutil
import tkinter
import customtkinter
from customtkinter import CTkFrame, filedialog, CTkLabel, CTkButton, CTkOptionMenu
from smct import ui_strings, config, multimonitortool, paths


class Application:
    def __init__(self):
        customtkinter.set_ctk_parent_class(tkinter.Tk)
        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("dark-blue")

        self.root_window = customtkinter.CTk()
        self.root_window.title(ui_strings.SHORT_NAME)
        self.root_window.resizable(False, False)
        self.root_window.protocol("WM_DELETE_WINDOW", self.exit_application)
        self.root_window.iconbitmap(paths.ASSETS_ICO_PATH)

        self.init_mmt_selection_frame()

    def exit_application(self):
        shutil.rmtree(paths.ASSETS_DIR_PATH, ignore_errors=True)
        for path in [
            paths.CONFIG_PATH,
            paths.LOG_PATH,
            paths.MMT_CONFIG_PATH,
            paths.MMT_CSV_PATH,
        ]:
            os.remove(path)
        self.root_window.destroy()
        sys.exit(1)

    def init_mmt_selection_frame(self):
        self.selection_frame = CTkFrame(master=self.root_window)
        self.selection_frame.pack(pady=10, padx=10, fill="both", expand=True)

        select_mmt_label = CTkLabel(
            text=ui_strings.SELECT_MMT_LABEL,
            master=self.selection_frame,
            justify=customtkinter.CENTER,
        )
        select_mmt_label.pack(pady=5, padx=5)

        browse_button = CTkButton(
            text=ui_strings.BROWSE_BUTTON,
            master=self.selection_frame,
            command=self.browse_button_callback,
        )
        browse_button.pack(pady=10, padx=10)

    def browse_button_callback(self):
        if exe_path := filedialog.askopenfilename(
            title=ui_strings.SELECT_MMT_LABEL,
            filetypes=[
                (paths.MMT_EXE_NAME.split(".", maxsplit=1)[0], paths.MMT_EXE_NAME)
            ],
        ):
            config.set_value(config.KEY_MMT_PATH, exe_path)
            self.selection_frame.destroy()
            self.init_monitor_selection_frame()
        else:
            print(ui_strings.NO_FILE_SELECTED)

    def init_monitor_selection_frame(self):
        # pylint: disable=attribute-defined-outside-init
        self.selection_frame = CTkFrame(master=self.root_window)
        self.selection_frame.pack(pady=10, padx=10, fill="both", expand=True)

        monitor_selection_label = CTkLabel(
            text=ui_strings.SELECT_MONITOR_LABEL,
            master=self.selection_frame,
            justify=customtkinter.CENTER,
        )
        monitor_selection_label.pack(pady=5, padx=5)

        monitor_selection_menu = CTkOptionMenu(
            self.selection_frame,
            values=multimonitortool.get_monitor_selection_list(),
        )
        monitor_selection_menu.pack(pady=10, padx=10)

        select_monitor_button = CTkButton(
            text=ui_strings.OK_BUTTON,
            master=self.selection_frame,
            command=lambda: self.select_monitor_button_callback(monitor_selection_menu),
        )
        select_monitor_button.pack(pady=10, padx=10)

    def select_monitor_button_callback(self, menu):
        menu_string = menu.get().split("|")
        config.set_value(config.KEY_MONITOR_NAME, menu_string[1].strip())
        config.set_value(config.KEY_MONITOR_SERIAL, menu_string[2].strip())
        multimonitortool.save_mmt_config()
        self.root_window.destroy()
