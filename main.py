# IMPORTS
import os
import time
from tkinter import Tk, mainloop, Label, LabelFrame, messagebox
from tkinter.ttk import Button
from TM1637 import FourDigit

# CREATE WINDOW
root = Tk()
root.geometry('750x500')

# TIME VARIABLES
NUM_MODS = 1
DIO = 38
CLK = 40
LUM = 1

TZ1 = 'America/Chicago'
TZ2 = 'UTC'

HR_24 = '24'
HR_12 = '12'

time_format = HR_24
display = FourDigit(dio=DIO, clk=CLK, lum=LUM)


# FUNCTIONS
def hr_format_12():
    msg = messagebox.showinfo("hello", "format changed to 12 hr")
    clicked
    
    if
    time_format = HR_12
    
    


def hr_format_24():
    msg = messagebox.showinfo("hello", "format changed to 24 hr")
    time_format = HR_24
        



# DISPLAY TIME ON MODULE
def displayTM(disp, tim, hrs):
    hour = tim.tm_hour
    minute = tim.tm_min

    if hrs == '12':
        hour = (tim.tm_hour % 12) or 12
    disp.show("%02d%02d" % (hour, minute))
    # disp.setColon(colon)


# CREATE LABEL FRAMES
temp_frame = LabelFrame(root, text='temperature', height=250, width=750, )
temp_frame.pack()
temp_frame.place(x=0, y=0)

humid_frame = LabelFrame(root, text='humidity', height=250, width=375)
humid_frame.pack()
humid_frame.place(x=0, y=250)

time_frame = LabelFrame(root, text='time', height=250, width=375)
time_frame.pack()
time_frame.place(x=375, y=250)

btn_24 = Button(time_frame, text='24 Hour Format', command=hr_format_24)
btn_24.place(x=30, y=10)

btn_12 = Button(time_frame, text='12 Hour Format', command=hr_format_12)
btn_12.place(x=200, y=10)




mainloop()

while True:
    cur = time.time()        
    os.environ["TZ"] = TZ1
    time.tzset()
    ct = time.localtime(cur)
    
    displayTM(display, ct, time_format)    
    time.sleep(0.5)
