#!/usr/bin/env python3

try:
    import tkinter as tk
except ImportError:
    print("Python-Tk is not installed. Please install it using your package manager (e.g., 'pip install tk') or system package manager (e.g., 'sudo apt install python3-tk')")
    exit(1)
from tkinter import ttk

def calculate_charge_time():
    try:
        remaining_battery = float(entry1.get())
        battery_capacity = float(entry2.get())
        charge_rate = float(entry3.get())
        result = (100 - remaining_battery) * battery_capacity / charge_rate / 100
        result_label.config(text="Total Time in Hours: " + str(result))
    except ValueError:
        result_label.config(text="Invalid input. Please enter numbers only.")

def calculate_range():
    try:
        battery_capacity_ah = float(battery_capacity_entry.get())
        motor_power_watts = float(motor_power_entry.get())
        battery_voltage = float(battery_voltage_entry.get())
        battery_percent = float(battery_percent_entry.get())
        rider_weight_equipment = float(rider_weight_entry.get())

        base_watts_per_mile = 19.95
        weight_factor = 1 + (rider_weight_equipment / 700)
        motor_power_factor = 1 + (motor_power_watts / 2000)
        watts_per_mile = base_watts_per_mile * weight_factor * motor_power_factor

        total_energy_wh = battery_capacity_ah * battery_voltage
        remaining_energy_wh = total_energy_wh * (battery_percent / 100)
        estimated_miles = remaining_energy_wh / watts_per_mile

        result_label.config(text=f"Estimated miles remaining: {estimated_miles:.2f} miles")
    except ValueError:
        result_label.config(text="Invalid input. Please enter numerical values.")

def show_frame(frame):
    frame.tkraise()

# Create the main window
root = tk.Tk()
root.title("Gobytego EV Tools v1.0")

# Create a container frame
container = tk.Frame(root)
container.pack(side="top", fill="both", expand=True)
root.geometry("400x300")

# Create frames for each calculator
charge_time_frame = tk.Frame(container)
range_frame = tk.Frame(container)

# Add frames to the container
for frame in (charge_time_frame, range_frame):
    frame.grid(row=0, column=0, sticky="nsew")

# Create a frame for the result label
result_label_frame = ttk.Frame(container)
result_label_frame.grid(row=1, column=0, sticky="nsew")

# Create a label to display the result
result_label = ttk.Label(result_label_frame, text="")
result_label.pack(side="bottom", fill="x", padx=10, pady=10)

# Create tabs
tab_control = ttk.Notebook(root)
tab1 = ttk.Frame(tab_control)
tab2 = ttk.Frame(tab_control)
tab_control.add(tab1, text='Charge Time')
tab_control.add(tab2, text='Range')
tab_control.pack(expand=1, fill='both')

# Create Charge Time Calculator Frame Elements
label1 = ttk.Label(tab1, text="Enter the Remaining Battery %:")
label1.grid(row=0, column=0, sticky="e")
entry1 = ttk.Entry(tab1)
entry1.grid(row=0, column=1)

label2 = ttk.Label(tab1, text="Enter the Battery Capacity (Ah):")
label2.grid(row=1, column=0, sticky="e")
entry2 = ttk.Entry(tab1)
entry2.grid(row=1, column=1)

label3 = ttk.Label(tab1, text="Enter the Charge Rate in Amps:")
label3.grid(row=2, column=0, sticky="e")
entry3 = ttk.Entry(tab1)
entry3.grid(row=2, column=1)

calculate_button_charge = ttk.Button(tab1, text="Calculate", command=calculate_charge_time)
calculate_button_charge.grid(row=3, column=0, columnspan=2)

# Create Range Estimator Frame Elements
battery_capacity_label = ttk.Label(tab2, text="Battery Capacity (Ah):")
battery_capacity_entry = ttk.Entry(tab2)

motor_power_label = ttk.Label(tab2, text="Motor Power (Watts):")
motor_power_entry = ttk.Entry(tab2)

battery_voltage_label = ttk.Label(tab2, text="Battery Voltage (Volts):")
battery_voltage_entry = ttk.Entry(tab2)

battery_percent_label = ttk.Label(tab2, text="Remaining Battery (%):")
battery_percent_entry = ttk.Entry(tab2)

rider_weight_label = ttk.Label(tab2, text="Rider Weight + Equipment (lbs):")
rider_weight_entry = ttk.Entry(tab2)

calculate_button_range = ttk.Button(tab2, text="Calculate", command=calculate_range)

# Grid layout for range estimator frame elements
battery_capacity_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
battery_capacity_entry.grid(row=0, column=1, padx=5, pady=5)

motor_power_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
motor_power_entry.grid(row=1, column=1, padx=5, pady=5)

battery_voltage_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")
battery_voltage_entry.grid(row=2, column=1, padx=5, pady=5)

battery_percent_label.grid(row=3, column=0, padx=5, pady=5, sticky="w")
battery_percent_entry.grid(row=3, column=1, padx=5, pady=5)

rider_weight_label.grid(row=4, column=0, padx=5, pady=5, sticky="w")
rider_weight_entry.grid(row=4, column=1, padx=5, pady=5)

calculate_button_range.grid(row=5, columnspan=2, padx=5, pady=5)

# Initially show the first tab
show_frame(charge_time_frame)

root.mainloop()
