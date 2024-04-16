import customtkinter
import tkinterDnD

from smct_pkg import gui

# https://github.com/TomSchimansky/CustomTkinter/tree/master/examples
# https://github.com/TomSchimansky/CustomTkinter

customtkinter.set_ctk_parent_class(tkinterDnD.Tk)

customtkinter.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme(
    "dark-blue"
)  # Themes: "blue" (standard), "green", "dark-blue"

app = customtkinter.CTk()
app.geometry("300x180")
app.title("CustomTkinter simple_example.py")


def button_callback():
    gui.select_multimonitortool()


frame = customtkinter.CTkFrame(master=app)
frame.pack(pady=20, padx=20, fill="both", expand=True)

select_multimonitortool_label = customtkinter.CTkLabel(
    text="Please select your MultiMonitorTool.exe",
    master=frame,
    justify=customtkinter.LEFT,
)
select_multimonitortool_label.pack(pady=10, padx=10)

browse_button = customtkinter.CTkButton(
    text="Browse...", master=frame, command=button_callback
)
browse_button.pack(pady=10, padx=10)


app.mainloop()

# pylint: disable=pointless-string-statement
"""
monitor_selection_menu = customtkinter.CTkOptionMenu(
    frame, values=["Option 1", "Option 2", "Option 42 long long long..."]
)
monitor_selection_menu.pack(pady=10, padx=10)
monitor_selection_menu.set("Select your monitor")
"""
