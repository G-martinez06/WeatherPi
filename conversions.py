import tkinter as tk
from tkinter import ttk
import Adafruit_DHT
from TM1637 import FourDigit
import time
#  Sensor Setup
DHTSensor = Adafruit_DHT.DHT11
GPIO_Pin = 23

# TM1637 Display Setup
try:
    display = FourDigit(clk=21, dio=20)
    display.clear()
    print("TM1637 display initialized.")
except Exception as e:
    print(f"[ERROR] Could not initialize TM1637 display: {e}")
    display = None

# Function to Read and Display Temp
def get_temperature():
    humid, temp_c = Adafruit_DHT.read_retry(DHTSensor, GPIO_Pin)

    if humid is not None and temp_c is not None:
        if unit.get() == "°F":
            temp_display = (temp_c * 9 / 5) + 32
        else:
            temp_display = temp_c

        result = f"Temp: {temp_display:.1f}{unit.get()}\nHumidity: {humid:.1f}%"
        result_label.config(text=result)
        print(f"[INFO] {result}")

        if display:
            display.clear()
            display.write_number(int(round(temp_display)))
    else:
        result_label.config(text="Sensor error")
        print("[WARN] Sensor failure")
        if display:
            display.clear()

# GUI Setup
root = tk.Tk()
root.title("Real-Time Temp Monitor")
root.geometry("300x200")

# Unit selection
unit = tk.StringVar(value="°C")
ttk.Label(root, text="Display Unit").pack()
ttk.Combobox(root, textvariable=unit, values=["°C", "°F"], state="readonly").pack(pady=5)

# Read Temp Button
ttk.Button(root, text="Get Temperature", command=get_temperature).pack(pady=10)

# Display Label
result_label = ttk.Label(root, text="", font=("Arial", 12))
result_label.pack(pady=10)

# Launch GUI
root.mainloop()
