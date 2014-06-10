# -*- coding: utf-8 -*-
from Tkinter import *
import re, urllib, os


def job():
    """
    Function:: job(arg1, arg2, arg3, arg4)
    Return:: Returns the output format and the correct error code for centreon.
    """

    htmlSource = urllib.urlopen('http://'+bus_ip.get()+'/1Wire/ReadTemperature.html?Address_Array='+probe_id.get()).read(200000)
    matchObj = re.findall(r'VALUE="(.*?)"',htmlSource,re.M|re.I)


    if matchObj != None:
        if float(matchObj[8]) >= float(warn.get()) :
            if float(matchObj[8]) >= float(crit.get()):
                result.set("[Critical]- Temperature :"+matchObj[8]+"°C | Temp="+matchObj[8]+"°C State=Critical")
            else:
                result.set("[Warning]- Temperature :"+matchObj[8]+"°C | Temp="+matchObj[8]+"°C State=Warning")
        else:
            result.set("[OK]- Temperature: "+matchObj[8]+"°C | Temp="+matchObj[8]+"°C State=Normal")
    else:
        result.set("[Error]- ProbeBus is probably unreachable. | Temp=0°C State=Error")


# Create main frame
main_window = Tk()
main_window.title('QMP - Query My Probe - v0.1')
main_window.wm_iconbitmap("@"+"ico/temperature.xbm")
main_window.resizable(0,0)

# [ Config Vars ] =========
probe_id = StringVar()
warn = IntVar()
crit = IntVar()
bus_ip = StringVar()
result = StringVar()


# Data Frame
Data_Frame = LabelFrame(main_window, borderwidth=2,relief=GROOVE, text='Data Biding : ')
Data_Frame.grid(row=0, column=0,padx=10,pady=10)

# Action Frame
Action_Frame = LabelFrame(main_window, borderwidth=2, relief=GROOVE, text='Action Zone : ')
Action_Frame.grid(row=0, column=1, padx=10, pady=10)

# Result Frame
Result_Frame = LabelFrame(main_window, borderwidth=2, relief=GROOVE, text='Results :')
Result_Frame.grid(row=2, column=0, padx=10, pady=10)

# Entry and labels widgets
LbProbeID = Label(Data_Frame, text='Probe ID :')
LbProbeID.grid(row=0, column=0, padx=5, pady=5)

ProbeID = Entry(Data_Frame, textvariable=probe_id)
ProbeID.grid(row=0, column=1, padx=5, pady=5)
ProbeID.focus_set()

LbWarn = Label(Data_Frame, text='Warning Threshold :')
LbWarn.grid(row=1, column=0, padx=5, pady=5)

Warn = Entry(Data_Frame, textvariable=warn)
Warn.grid(row=1, column=1, padx=5, pady=5)

LbCrit = Label(Data_Frame, text='Critical Threshold ;')
LbCrit.grid(row=2, column=0, padx=5, pady=5)

Crit = Entry(Data_Frame, textvariable=crit)
Crit.grid(row=2, column=1, padx=5, pady=5)

LbBus = Label(Data_Frame, text='Bus IP :')
LbBus.grid(row=3, column=0, padx=5, pady=5)

Bus_ip = Entry(Data_Frame, textvariable=bus_ip)
Bus_ip.grid(row=3, column=1, padx=5, pady=5)


# Action buttons
launch_button = Button(Action_Frame, text='Gotcha!', command=job)
launch_button.grid(row=0, column=0, padx=5, pady=5)

quit_button = Button(Action_Frame, text='Quit', command=main_window.destroy)
quit_button.grid(row=1, column=0, padx=5, pady=5)

# Show results
LbResult = Label(Result_Frame, text='Results not available yet...', textvariable=result)
LbResult.pack(side=LEFT, padx=5, pady=5)


main_window.mainloop()