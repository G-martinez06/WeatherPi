import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import RPi.GPIO as GPIO
import Adafruit_DHT
import time
 
# Adafruit_DHT.DHT22, or Adafruit_DHT.AM2302.
DHTSensor = Adafruit_DHT.DHT11
 
# The pin which is connected with the sensor will be declared here
GPIO_Pin = 23

from collections import deque #for managing list size

#CHANGE LATER
import random #change to adafruit humidity
import time #change to clock time
start = time.time() #change to when the program loads

#GUI
root = tk.Tk()
root.title("Humidity")
root.geometry("700x500")
frame = ttk.Frame(root)
frame.pack(fill=tk.BOTH) #delete GUI once added into larger gui

#VALUES
humidityVal = deque(maxlen=30)
seconds = deque(maxlen=30)

#GRAPH
graph = Figure(figsize=(6, 4),
               dpi=100) #Change figsize to let the graph stay in the corner
                        #and change dpi if line is too small
axis = graph.add_subplot(111)
axis.set_title("Humidity Over Time") #Possibly delete all labels except this
axis.set_xlabel("Time (s)")
axis.set_ylabel("Humidity %")

canvas = FigureCanvasTkAgg(graph, master=frame)
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True) #change to fit bigger GUI
canvas.draw()

def updater():
    current = time.strftime("%H:%M:%S")
    seconds.append(current)

    humidity, temper = Adafruit_DHT.read_retry(DHTSensor, GPIO_Pin)
    humidityVal.append(humidity)

    #GRAPH DRAWING
    axis.clear()
    axis.vlines(seconds, [0], humidityVal, color= 'green', linewidth=5)
    axis.set_title("Humidity Over Time")
    axis.set_xlabel("Time (s)")
    axis.set_ylabel("Humidity (%)")
    axis.set_ylim(0, 100) #0 to 100 percent humidity
    axis.grid(True)

    canvas.draw()
    root.after(2000, updater) #change to reflect amount of time before next reading


updater()
root.mainloop()
