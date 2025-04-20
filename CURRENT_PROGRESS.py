# IMPORTS
import os
import time
import tkinter as tk
from tkinter import Tk, mainloop, LabelFrame, LEFT, BOTH
from tkinter.ttk import Button, Combobox
from TM1637 import FourDigit
import Adafruit_DHT
import time

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from collections import deque #for managing list size

start = time.time() #change to when the program loads

# CREATE WINDOW
root = Tk()
root.geometry('700x300')
DHTSensor = Adafruit_DHT.DHT11
GPIO_Pin = 4


# TIME VARIABLES
NUM_MODS = 1
DIO = 38
CLK = 40
LUM = 1

tz_var = tk.StringVar()

display = FourDigit(dio=DIO, clk=CLK, lum=LUM)
    
global time_format
time_format = '12'


# FUNCTIONS
def hr_format_12():
    display.erase()

    global time_format
    time_format = '12'


def hr_format_24():
    display.erase()

    global time_format
    time_format = '24'


def set_tz():
    display.erase()
    tz = tz_var.get()

    os.environ["TZ"] = tz
    time.tzset()
    
    print("tz: " + tz)
    
    tz_var.set("")


# DISPLAY TIME ON MODULE
def displayTM(disp, tim, hrs):
    hour = tim.tm_hour
    minute = tim.tm_min

    if hrs == '12':
        hour = (tim.tm_hour % 12) or 12
    disp.show("%02d%02d" % (hour, minute))


def get_temperature():
    humid, temp_c = Adafruit_DHT.read_retry(DHTSensor, GPIO_Pin)

    if humid is not None and temp_c is not None:
        if temp_unit.get() == "°F":
            temp_display = (temp_c * 9 / 5) + 32
        else:
            temp_display = temp_c

        result = f"Temp: {temp_display:.1f}{temp_unit.get()}\nHumidity: {humid:.1f}%"
        result_label.config(text=result)
        print(f"[INFO] {result}")

    else:
        result_label.config(text="Sensor error")
        print("[WARN] Sensor failure")


def update():
    cur = time.time()
    ct = time.localtime(cur)

    displayTM(display, ct, time_format)
    time.sleep(0.5)
    
    root.after(1000, update)

#######################################################################################################################
#######################################################################################################################

# CREATE LABEL
temp_frame = LabelFrame(root)
temp_frame.pack(side=LEFT, expand=True, fill=BOTH)

# Unit selection
temp_unit = tk.StringVar(value="°C")

temp_label = tk.Label(temp_frame, text="Display Unit")
temp_label.pack()

temp_cb = Combobox(temp_frame, textvariable=temp_unit, values=["°C", "°F"], state="readonly")
temp_cb.pack()

# Read Temp Button
temp_btn = Button(temp_frame, text="Get Temperature", command=get_temperature)
temp_btn.pack()

# Display Label
result_label = tk.Label(temp_frame, text="", font=("Arial", 12))
result_label.pack()

#######################################################################################################################
#######################################################################################################################

humid_frame = LabelFrame(root)
humid_frame.pack(side=LEFT, expand=True, fill=BOTH)

frame = tk.Frame(humid_frame)
frame.pack() #delete GUI once added into larger gui

#VALUES
humidityVal = deque(maxlen=30)
seconds = deque(maxlen=30)

#GRAPH
graph = Figure(figsize=(6, 4),
               dpi=60) #Change figsize to let the graph stay in the corner
                        #and change dpi if line is too small
axis = graph.add_subplot(111)
axis.set_title("Humidity Over Time") #Possibly delete all labels except this
axis.set_xlabel("Time (s)")
axis.set_ylabel("Humidity %")

canvas = FigureCanvasTkAgg(graph, master=frame)
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True) #change to fit bigger GUI
canvas.draw()


def updater():
    current = time.strftime("%S")
    seconds.append(current)

    humidity, t = Adafruit_DHT.read_retry(DHTSensor, GPIO_Pin)
    humidityVal.append(humidity)

    #GRAPH DRAWING
    axis.clear()
    axis.plot(seconds, humidityVal, color='green', linewidth=5)
    axis.set_title("Humidity Over Time")
    axis.set_xlabel("Time (s)")
    axis.set_ylabel("Humidity (%)")
    axis.set_ylim(0, 100) #0 to 100 percent humidity

    axis.grid(True)

    canvas.draw()
    root.after(2000, updater) #change to reflect amount of time before next reading


updater()

#######################################################################################################################
#######################################################################################################################

time_frame = LabelFrame(root)
time_frame.pack(side=LEFT, expand=True, fill=BOTH)

time_text = tk.Text(time_frame, height=5, width=70, font=("Courier New", 7))
time_text.pack()

tt = """This section controls the TM1637 module. It can toggle the clock format and change the timezone. To change the timezone"""
time_text.insert(tk.END, tt)

btn_label = tk.Label(time_frame, text="TOGGLE TIME FORMAT:")
btn_label.pack()

btn_24 = Button(time_frame, text='24 Hour Format', command=hr_format_24)
btn_24.pack()

btn_12 = Button(time_frame, text='12 Hour Format', command=hr_format_12)
btn_12.pack()

tz_label = tk.Label(time_frame, text="CHANGE TIME ZONE:")
tz_label.pack()

tz_label2 = tk.Label(time_frame, text="New Time Zone:")
tz_label2.pack()
tz = tk.Entry(time_frame, textvariable=tz_var)
tz.pack()
tz_sub = Button(time_frame, text='Submit', command=set_tz)
tz_sub.pack()

#######################################################################################################################
#######################################################################################################################

update()
mainloop()
display.erase()
