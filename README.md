PC Charging Monitor
Last Updated: June 16, 2025

The PC Charging Monitor is a graphical application built with Python that provides real-time monitoring of your laptop's battery status. It displays charger status, battery percentage, capacity, charging/discharge current, time to full, and a detailed analysis, visualized with a live bar chart. It also maintains a history log of analysis data.

Overview
This application uses tkinter for the GUI, psutil for battery information, and matplotlib for real-time bar chart visualization. It is designed for Windows systems with optional support for wmi to retrieve detailed battery data. The script can be converted into a standalone .exe application for easy distribution.

Features
Real-Time Monitoring: Displays charger status, battery percentage, capacity, current, time to full, and analysis updated every second.
Bar Chart Visualization: Shows "Current Battery Level" (blue) and "Used Battery Level" (red) over the last 60 seconds.
Analysis History Log: Records analysis data with timestamps in analysis_history.log and displays the last 5 entries in the GUI.
Automatic Package Installation: Installs required dependencies (psutil, matplotlib, wmi on Windows) during execution.
Executable Conversion: Includes a build script to create a standalone .exe installer.
Prerequisites
Operating System: Windows (recommended due to wmi dependency).
Python: Version 3.6 or higher.
Internet Connection: Required for initial package installation via pip.
Optional: Inno Setup (for installer creation) available at https://jrsoftware.org/isinfo.php.
Installation
Clone or Download:
Download the repository or copy power_monitor.py and install_builder.py into a single directory.
Install Dependencies:
Run python power_monitor.py to automatically install psutil, matplotlib, and wmi (on Windows) if not already present.
Build the Executable:
Open a command prompt in the directory containing the scripts.
Run python install_builder.py.
This will:
Install pyinstaller and build a single .exe file in the dist folder.
Clean up temporary files and generate an installer (dist\PC_Charging_Monitor_Installer.exe).
If Inno Setup is not installed, download and install it, then retry.
Install the Application:
Run dist\PC_Charging_Monitor_Installer.exe on a Windows machine to install the application.
Usage
Run the Script:
Execute python power_monitor.py to launch the GUI directly (for development/testing).
Run the Installed App:
After installation, launch "PC Charging Monitor" from the Start menu or desktop shortcut.
Interface:
Charger Status: Indicates if the charger is connected or disconnected.
Battery Percentage: Shows the current battery level.
Battery Capacity: Displays the design capacity (in mAh).
Charging/Discharge Current: Estimates current in amperes.
Time to Full: Estimates time to full charge or remaining time.
Analysis: Provides a summary including health and capacity.
Bar Chart: Visualizes current and used battery levels.
History Log: Shows the last 5 logged analysis entries.
Customization
Adjust Parameters:
Modify charger_power (default 65.0 W) and charger_voltage (default 15.0 V) in get_charging_info to match your hardware.
Change data_points (default 60) in __init__ to adjust the chart's time window.
Icon:
Place an icon.ico file in the directory to customize the .exe icon.
Limitations
Windows-Only: Relies on wmi for detailed battery data, limiting compatibility to Windows.
Anti-Virus: The generated .exe may be flagged by antivirus software; inform users to allow it.
Battery Data: Accuracy depends on psutil; desktops without batteries may show limited data.
Inno Setup: Required for installer creation; manual installation needed if missing.
Troubleshooting
Dependency Errors: Ensure an internet connection is available for pip installation. Re-run the script if packages fail to install.
Inno Setup Not Found: Install Inno Setup from https://jrsoftware.org/isinfo.php and retry install_builder.py.
Runtime Issues: Check the console output for errors. Share system details (e.g., Windows version, Python version) for support.
Log File: If analysis_history.log is missing, ensure write permissions in the script directory.
License
This project is provided as-is without a formal license. Feel free to modify and distribute, but usage is at your own risk.

Contact
For questions or issues, please reach out via the repository (if hosted) or provide feedback through the original source.
