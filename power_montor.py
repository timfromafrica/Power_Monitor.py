import subprocess
import sys
import time
import importlib.util
import platform
import tkinter as tk
from tkinter import ttk
import psutil
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Windows-specific import for WMI
if platform.system() == "Windows":
    try:
        import wmi
    except ImportError:
        wmi = None
else:
    wmi = None

# Function to install required packages
def install_packages(packages):
    for package in packages:
        if not importlib.util.find_spec(package):
            print(f"Installing {package}...")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", package, "--user"])
            except Exception as e:
                print(f"Failed to install {package}: {e}")
                sys.exit(1)

# List of required packages
required_packages = ['psutil', 'matplotlib']
if platform.system() == "Windows":
    required_packages.append('wmi')
install_packages(required_packages)

# GUI class
class PowerMonitorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PC Charging Monitor")
        self.root.geometry("600x550")  # Adjusted for history log

        # Styling
        style = ttk.Style()
        style.configure("TLabel", font=("Helvetica", 12))
        style.configure("Header.TLabel", font=("Helvetica", 16, "bold"))
        style.configure("Analysis.TLabel", font=("Helvetica", 10, "italic"))
        style.configure("Log.TLabel", font=("Helvetica", 10))

        # Layout
        self.header_label = ttk.Label(root, text="PC Charging Monitor", style="Header.TLabel")
        self.header_label.pack(pady=10)

        self.charger_label = ttk.Label(root, text="Charger Status: N/A")
        self.charger_label.pack(pady=5)

        self.battery_label = ttk.Label(root, text="Battery Percentage: N/A")
        self.battery_label.pack(pady=5)

        self.capacity_label = ttk.Label(root, text="Battery Capacity: N/A")
        self.capacity_label.pack(pady=5)

        self.current_label = ttk.Label(root, text="Charging Current: N/A")
        self.current_label.pack(pady=5)

        self.discharge_label = ttk.Label(root, text="Discharge Current: N/A")
        self.discharge_label.pack(pady=5)

        self.time_label = ttk.Label(root, text="Time to Full: N/A")
        self.time_label.pack(pady=5)

        self.analysis_label = ttk.Label(root, text="Analysis: Loading...", style="Analysis.TLabel", wraplength=350)
        self.analysis_label.pack(pady=10)

        # Matplotlib bar chart
        self.fig, self.ax = plt.subplots(figsize=(8, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().pack(pady=10, fill="both", expand=True)

        self.ax.set_title("Battery Level Analysis")
        self.ax.set_xlabel("Time (s)")
        self.ax.set_ylabel("Percentage (%)")
        self.ax.grid(True)
        self.ax.set_ylim(0, 100)

        self.current_bars = []
        self.used_bars = []
        self.time_data = []

        self.data_points = 60  # 60 seconds (1 minute) of data

        # History log display
        self.log_label = ttk.Label(root, text="History Log: Loading...", style="Log.TLabel", wraplength=550)
        self.log_label.pack(pady=5)

        # Start updating
        self.update_data()

    def get_battery_capacity(self):
        """Retrieve original (design) battery capacity in mAh."""
        try:
            if platform.system() == "Windows" and wmi:
                c = wmi.WMI()
                for battery in c.Win32_Battery():
                    if battery.DesignCapacity:
                        # DesignCapacity is in mWh, convert to mAh (assume 15V)
                        voltage = 15.0  # Typical laptop battery voltage
                        return battery.DesignCapacity / voltage
            # Fallback for Linux/macOS or if WMI fails
            return 4000.0  # Assume typical 4000 mAh laptop battery
        except Exception:
            return 4000.0  # Fallback capacity

    def get_charging_info(self):
        try:
            battery = psutil.sensors_battery()
            if battery is None:
                return "Unknown", "N/A", "N/A", "N/A", "N/A", "N/A", "No battery detected."

            # Charger status and battery percentage
            plugged = "Connected" if battery.power_plugged else "Disconnected"
            percent = f"{battery.percent:.1f}%"

            # Get original battery capacity
            design_capacity_mah = self.get_battery_capacity()
            capacity_str = f"{design_capacity_mah:.0f} mAh"

            if battery.power_plugged:
                # Assume charger power (65W) and voltage (15V) for current estimation
                charger_power = 65.0  # Watts (modify based on your charger)
                charger_voltage = 15.0  # Volts (modify based on your charger)
                current_ma = (charger_power / charger_voltage) * 1000  # Convert A to mA
                current_str = f"{current_ma / 1000:.2f} A"
                discharge_str = "N/A"  # No discharge when charging

                # Calculate time to full charge
                remaining_capacity = design_capacity_mah * (100 - battery.percent) / 100
                if current_ma > 0:
                    time_hours = remaining_capacity / current_ma
                    time_minutes = int(time_hours * 60)
                    time_str = f"{time_minutes} minutes"
                else:
                    time_str = "Unknown"

                # Analysis
                health = "Good" if battery.percent > 20 else "Poor"
                analysis = (
                    f"Charging at {current_ma / 1000:.2f} A. "
                    f"Time to full: {time_str}. "
                    f"Battery health: {health}. "
                    f"Original capacity: {design_capacity_mah:.0f} mAh."
                )
            else:
                current_str = "0.00 A"
                time_str = "N/A"
                # Estimate discharge current
                remaining_capacity = design_capacity_mah * (battery.percent / 100)
                if battery.secsleft and battery.secsleft != psutil.POWER_TIME_UNKNOWN and battery.secsleft != psutil.POWER_TIME_UNLIMITED:
                    time_hours = battery.secsleft / 3600  # Convert seconds to hours
                    if time_hours > 0:
                        discharge_ma = remaining_capacity / time_hours
                        discharge_str = f"{discharge_ma / 1000:.2f} A"
                    else:
                        discharge_str = "N/A"
                else:
                    discharge_str = "N/A"

                analysis = (
                    f"Charger disconnected. "
                    f"Discharge current: {discharge_str}. "
                    f"Estimated time remaining: {battery.secsleft // 60 if battery.secsleft else 'N/A'} minutes. "
                    f"Battery health: {'Good' if battery.percent > 20 else 'Poor'}. "
                    f"Original capacity: {design_capacity_mah:.0f} mAh."
                )

            # Append to history log
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            with open("analysis_history.log", "a") as log_file:
                log_file.write(f"{timestamp} - {analysis}\n")

            return plugged, percent, capacity_str, current_str, discharge_str, time_str, analysis
        except Exception as e:
            return "Error", "N/A", "N/A", "N/A", "N/A", "N/A", f"Error accessing battery data: {str(e)}"

    def update_data(self):
        charger_status, battery_percent, capacity, current, discharge, time_to_full, analysis = self.get_charging_info()
        self.charger_label.config(text=f"Charger Status: {charger_status}")
        self.battery_label.config(text=f"Battery Percentage: {battery_percent}")
        self.capacity_label.config(text=f"Battery Capacity: {capacity}")
        self.current_label.config(text=f"Charging Current: {current}")
        self.discharge_label.config(text=f"Discharge Current: {discharge}")
        self.time_label.config(text=f"Time to Full: {time_to_full}")
        self.analysis_label.config(text=f"Analysis: {analysis}")

        # Update chart data
        self.time_data.append(time.time())
        if len(self.time_data) > self.data_points:
            self.time_data.pop(0)
            for bar in self.current_bars:
                bar.remove()
            for bar in self.used_bars:
                bar.remove()
            self.current_bars.clear()
            self.used_bars.clear()

        # Parse and add data
        percent_value = float(battery_percent.strip("%")) if "%" in battery_percent else 0.0
        used_value = 100.0 - percent_value

        # Create bars for the current time point
        x = len(self.time_data) - 1
        self.current_bars.append(self.ax.bar(x, percent_value, color="#1E90FF", label="Current Battery Level" if not self.current_bars else ""))
        self.used_bars.append(self.ax.bar(x, used_value, bottom=percent_value, color="#FF4500", label="Used Battery Level" if not self.used_bars else ""))

        # Update plot limits and labels
        self.ax.set_xlim(-1, self.data_points)
        self.ax.set_ylim(0, 100)
        self.ax.legend()

        # Update history log display (last 5 entries)
        try:
            with open("analysis_history.log", "r") as log_file:
                lines = log_file.readlines()[-5:]  # Last 5 entries
                self.log_label.config(text="History Log:\n" + "".join(lines))
        except FileNotFoundError:
            self.log_label.config(text="History Log: No data yet.")

        self.canvas.draw()

        self.root.after(1000, self.update_data)  # Update every 1 second

    def __del__(self):
        # Ensure log file is closed properly on exit
        pass

# Main execution
if __name__ == "__main__":
    root = tk.Tk()
    app = PowerMonitorApp(root)
    root.mainloop()
