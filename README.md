# SimpleMonitorControlTray

Older flat TVs which can be easily used as a optional monitor in Windows. However, the TV cannot detect if it's receiving a signal and therefore doesn't turn on by itself. If you have any windows on the turned off TV you can't access them easily without opening the Windows Settings.

SimpleMonitorControlTray is a small Python program that tries to solve this problem by letting you to easily enable and disable a specified monitor using MultiMonitorTool.exe. Simply click the icon in the system tray to toggle the monitor state.

## Features

- Toggle the state of a specified monitor/TV with a single click.
- Save monitor layout that will be restored when enabling a monitor (to keep orientation, positioning, etc.)

Monitor turned on: <br>
![image](https://github.com/wrecks-code/SimpleMonitorControlTray/assets/29825723/cdad92e9-95b9-4a47-b8d4-4a691c18fef4)

Monitor turned off: <br>
![image](https://github.com/wrecks-code/SimpleMonitorControlTray/assets/29825723/319efc4a-24e0-4ee0-a346-15fa44001169)


## Requirements

- [MultiMonitorTool](https://www.nirsoft.net/utils/multimonitortool-x64.zip)
- Windows OS

## Installation

1. Download the [latest release](https://github.com/wrecks-code/SimpleMonitorControlTray/releases/latest) and unzip anywhere
2. Download MultiMonitorTool and unzip anywhere

## Usage

1. Double-click `SimpleMonitorControlTray.exe` to start.
2. The program will prompt you to Browse for your `MultiMonitorTool.exe` path<br>

   ![image](https://github.com/wrecks-code/SimpleMonitorControlTray/assets/29825723/753a59a9-02f0-458d-8e0d-ac7fe3789a51)

3. Select the monitor that will be toggled by clicking the tray icon<br>

   ![image](https://github.com/wrecks-code/SimpleMonitorControlTray/assets/29825723/9561bd49-7f1a-4bb1-bafc-4ced81ab40d5)

5. More options can be found by right clicking the tray icon
   
   ![image](https://github.com/wrecks-code/SimpleMonitorControlTray/assets/29825723/40826a9e-c197-4c9d-9b5e-62dd208503c9)


## Notes

- "Startup with Windows" places a regkey inside `Computer\HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run`, it can be removed by clicking it again.
- A default layout will be saved on first startup, you can overwrite it by right-clicking and selecting "Save current monitor layout".
- If you encounter any issues or have suggestions for improvements, feel free to open an issue or submit a pull request.

- I used this project mainly to get a feel for python developing. I learned a lot from this.

## License

This project is released under the GNU General Public License (GPL) version 3.0. See the [LICENSE](LICENSE) file for details.

---

GNU General Public License (GPL) version 3.0

[GPL License Text](https://www.gnu.org/licenses/gpl-3.0.html)
