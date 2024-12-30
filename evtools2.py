import tkinter as tk
from tkinter import ttk
import json

class MyApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("EVTools")

        # Load saved data (if available)
        try:
            with open('saved_data.json', 'r') as f:
                self.saved_data = json.load(f)
        except FileNotFoundError:
            self.saved_data = {
                'rider_weight': '',
                'motor_wattage': '',
                'battery_voltage': '',
                'battery_capacity': ''
            }

        # Create notebook (tabs)
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill="both")

        # Tab 1: Input Fields
        self.tab1 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab1, text="Input")

        # Input fields for Tab 1
        self.rider_weight_var = tk.StringVar(value=self.saved_data['rider_weight'])
        self.motor_wattage_var = tk.StringVar(value=self.saved_data['motor_wattage'])
        self.battery_voltage_var = tk.StringVar(value=self.saved_data['battery_voltage'])
        self.battery_capacity_var = tk.StringVar(value=self.saved_data['battery_capacity'])

        ttk.Label(self.tab1, text="Rider Weight + Gear (LBS):").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        ttk.Entry(self.tab1, textvariable=self.rider_weight_var).grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.tab1, text="Motor Wattage (W):").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        ttk.Entry(self.tab1, textvariable=self.motor_wattage_var).grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self.tab1, text="Battery Voltage (V):").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        ttk.Entry(self.tab1, textvariable=self.battery_voltage_var).grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(self.tab1, text="Battery Capacity (Ah):").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        ttk.Entry(self.tab1, textvariable=self.battery_capacity_var).grid(row=3, column=1, padx=5, pady=5)

        # Save button
        ttk.Button(self.tab1, text="Save", command=self.save_data).grid(row=4, column=0, columnspan=2, padx=5, pady=5)

        # Tab 2: Charge Calculation
        self.tab2 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab2, text="Charge")

        # Input fields for Tab 2
        self.remaining_battery_var = tk.StringVar()
        self.charger_amp_var = tk.StringVar()
        self.charge_time_var = tk.StringVar()

        ttk.Label(self.tab2, text="Remaining Battery (%):").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        ttk.Entry(self.tab2, textvariable=self.remaining_battery_var).grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.tab2, text="Charger Amperage (A):").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        ttk.Entry(self.tab2, textvariable=self.charger_amp_var).grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self.tab2, text="Estimated Charging Time (hours):").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        ttk.Label(self.tab2, textvariable=self.charge_time_var).grid(row=2, column=1, padx=5, pady=5)

        # Calculate button
        ttk.Button(self.tab2, text="Calculate", command=self.calculate_charge_time).grid(row=3, column=0, columnspan=2, padx=5, pady=5)

        # Tab 3: Range Calculation
        self.tab3 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab3, text="Range")

        # Input field for Tab 3
        self.battery_percent_var = tk.StringVar()
        self.estimated_range_var = tk.StringVar()

        ttk.Label(self.tab3, text="Battery Percentage Remaining (%):").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        ttk.Entry(self.tab3, textvariable=self.battery_percent_var).grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.tab3, text="Estimated Range (miles):").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        ttk.Label(self.tab3, textvariable=self.estimated_range_var).grid(row=1, column=1, padx=5, pady=5)

        # Calculate button
        ttk.Button(self.tab3, text="Calculate", command=self.calculate_range).grid(row=2, column=0, columnspan=2, padx=5, pady=5)

    def save_data(self):
        self.saved_data = {
            'rider_weight': self.rider_weight_var.get(),
            'motor_wattage': self.motor_wattage_var.get(),
            'battery_voltage': self.battery_voltage_var.get(),
            'battery_capacity': self.battery_capacity_var.get()
        }

        with open('saved_data.json', 'w') as f:
            json.dump(self.saved_data, f)

    def calculate_charge_time(self):
        try:
            remaining_battery = float(self.remaining_battery_var.get())
            capacity = float(self.battery_capacity_var.get())
            amp = float(self.charger_amp_var.get())

            if 0 <= remaining_battery <= 100 and amp > 0:
                charge_percentage = 100 - remaining_battery
                charge_time = (charge_percentage * capacity) / (amp * 100)
                self.charge_time_var.set("{:.2f}".format(charge_time))
            else:
                self.charge_time_var.set("Invalid input")
        except ValueError:
            self.charge_time_var.set("Invalid input")

    def calculate_range(self):
        try:
            battery_capacity = float(self.battery_capacity_var.get())
            motor_power = float(self.motor_wattage_var.get())
            battery_voltage = float(self.battery_voltage_var.get())
            battery_percent = float(self.battery_percent_var.get())
            rider_weight_equipment = float(self.rider_weight_var.get())

            base_watts_per_mile = 19.95
            weight_factor = 1 + (rider_weight_equipment / 700)
            motor_power_factor = 1 + (motor_power / 2000)
            watts_per_mile = base_watts_per_mile * weight_factor * motor_power_factor

            total_energy_wh = battery_capacity * battery_voltage
            remaining_energy_wh = total_energy_wh * (battery_percent / 100)
            estimated_miles = remaining_energy_wh / watts_per_mile

            self.estimated_range_var.set("{:.2f}".format(estimated_miles))
        except ValueError:
            self.estimated_range_var.set("Invalid input")

if __name__ == "__main__":
    app = MyApplication()
    app.mainloop()
