import tkinter as tk
from tkinter import filedialog, messagebox


def select_multimonitortool():
    """Opens a file explorer window to select multimonitortool.exe"""
    global multimonitortool_path
    multimonitortool_path = filedialog.askopenfilename(
        title="Select multimonitortool.exe",
        filetypes=[("Multimonitor Tool", "multimonitortool.exe")],
    )
    if not multimonitortool_path:
        print("No file selected. Please select multimonitortool.exe")
        return

    # Update UI with selected path (optional)
    selected_file_label.config(
        text=f"Selected Tool: {multimonitortool_path.split('/')[-1]}"
    )
    show_monitor_selection()  # Call function to show monitor selection window


def show_monitor_selection():
    """Creates a new window to select a monitor"""
    monitor_window = tk.Tk()
    monitor_window.title("Select Monitor")

    # Modern UI (limited customization with tkinter)
    monitor_window.geometry("300x150")  # Set window size

    # Option buttons (replace with your actual monitor list)
    monitor_list = ["Monitor 1", "Monitor 2", "Monitor 3"]  # Replace with your list

    selected_monitor_var = tk.StringVar(monitor_window)
    selected_monitor_var.set(monitor_list[0])  # Set default selection

    monitor_dropdown = tk.OptionMenu(
        monitor_window, selected_monitor_var, *monitor_list
    )
    monitor_dropdown.pack(pady=10)

    confirm_button = tk.Button(
        monitor_window,
        text="Confirm",
        command=lambda: print(f"Selected Monitor: {selected_monitor_var.get()}"),
    )  # Replace print with your logic
    confirm_button.pack(pady=10)

    monitor_window.mainloop()  # Start the event loop for the window


def show_initial_message():
    """Displays a message box before user selection"""
    messagebox.showinfo(
        title="Welcome!",
        message="In order to use this program, please select your MultiMonitorTool.exe",
    )


def show_menu():
    """Creates a simple window with a menu"""
    menu_window = tk.Tk()
    menu_window.title("Multimonitor Tool Options")

    # Modern UI (limited customization with tkinter)
    menu_window.geometry("300x150")  # Set window size

    # Option buttons (replace with your actual options)
    option1_button = tk.Button(
        menu_window, text="Option 1", command=lambda: print("Option 1 selected")
    )
    option2_button = tk.Button(
        menu_window, text="Option 2", command=lambda: print("Option 2 selected")
    )

    option1_button.pack(pady=10)
    option2_button.pack(pady=10)

    menu_window.mainloop()  # Start the event loop for the window


# Main program flow
multimonitortool_path = None  # Global variable to store selected path

# Initial message
show_initial_message()
select_multimonitortool()

# Setup window
root = tk.Tk()
root.title("Multimonitor Tool Setup")

# Selected file label (optional)
selected_file_label = tk.Label(root, text="")
selected_file_label.pack(pady=5)

# Select button
select_button = tk.Button(root, text="Browse...", command=select_multimonitortool)
select_button.pack(pady=10)

# Option button to launch menu (hidden initially)
menu_button = tk.Button(
    root, text="Show Options", command=show_menu
)  # Placeholder, not used here
menu_button.pack(pady=10)
menu_button.pack_forget()  # Hide the button initially

# Run the main event loop (hidden window)
root.withdraw()  # Hide the main window

if __name__ == "__main__":
    root.mainloop()  # Start the event loop only after selection
