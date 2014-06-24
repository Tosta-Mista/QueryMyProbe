# -*- coding: utf-8 -*-
from Tkinter import *
import re
import urllib
import subprocess


def job():
    """
    Job Function
    :return: Returns the output format and the correct error code for centreon.
    """
    htmlSource = urllib.urlopen('http://' + bus_ip.get() + '/1Wire/ReadTemperature.html?Address_Array=' +
                                probe_id.get()).read(200000)
    matchObj = re.findall(r'VALUE="(.*?)"', htmlSource, re.M | re.I)

    if matchObj is not None:
        if float(matchObj[8]) >= float(warn.get()):
            if float(matchObj[8]) >= float(crit.get()):
                result.set("[Critical]- Temperature :" + matchObj[8] + "°C | Temp=" + matchObj[8] + "°C State=Critical")
            else:
                result.set("[Warning]- Temperature :" + matchObj[8] + "°C | Temp=" + matchObj[8] + "°C State=Warning")
        else:
            result.set("[OK]- Temperature: " + matchObj[8] + "°C | Temp=" + matchObj[8] + "°C State=Normal")
    else:
        result.set("[Error]- ProbeBus is probably unreachable. | Temp=0°C State=Error")


def scan():
    """
    Scan Function
    :return: Returns a list of items we can put directly through.
    """

    cmd_line = "curl -q \"http://"+str(bus_ip.get())+"/1Wire/Search.html\" 2>/dev/null | sed --silent -e 's/.*<INPUT.*NAME=\"Address_\(.*\)\".*VALUE=\"\(.*\)\".*./\2/p' | sed -e'/9D00000013407027/d'"
    process = subprocess.Popen(cmd_line, shell=True, stdout=subprocess.PIPE)
    out, err = process.communicate()
    for line in out:
        probelist.insert(END, str(line))


# Create main frame
main_window = Tk()
main_window.title('QMP - Query My Probe - v0.1')
main_window.wm_iconbitmap("@" + "ico/temperature.xbm")
main_window.resizable(0, 0)

# Config Vars
probe_id = StringVar()
warn = IntVar()
crit = IntVar()
bus_ip = StringVar()
result = StringVar()


# Data Frame
Data_Frame = LabelFrame(main_window, borderwidth=2, relief=GROOVE, text='Data Biding :')
Data_Frame.grid(row=0, column=0, padx=5, pady=5)

# Result Frame
Result_Frame = LabelFrame(main_window, borderwidth=2, relief=GROOVE, text='Results :')
Result_Frame.grid(row=1, column=0, padx=5, pady=5)

# Action Frame
Action_Frame = LabelFrame(main_window, borderwidth=2, relief=GROOVE)
Action_Frame.grid(row=0, column=1, padx=5, pady=5)

# Entry and labels widgets
LbProbeIDList = Label(Data_Frame, text='Probe List')
LbProbeIDList.grid(row=4, column=0, padx=5, pady=5)

probelist = Listbox(Data_Frame)
probelist.grid(row=4, column=1, padx=5, pady=5, sticky=N+E+S+W)

scrollbar = Scrollbar(probelist)
scrollbar.grid(column=1, sticky=N+S)

probelist.config(yscrollcommand=scrollbar.set)
probelist.columnconfigure(0, weight=3)
scrollbar.config(command=probelist.yview)


LbProbeID = Label(Data_Frame, text='Probe ID :')
LbProbeID.grid(row=3, column=0, padx=5, pady=5)

ProbeID = Entry(Data_Frame, textvariable=probe_id)
ProbeID.grid(row=3, column=1, padx=5, pady=5)
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
LbBus.grid(row=0, column=0, padx=5, pady=5)

Bus_ip = Entry(Data_Frame, textvariable=bus_ip)
Bus_ip.grid(row=0, column=1, padx=5, pady=5)


# Action buttons
launch_button = Button(Action_Frame, text='Probe', command=job)
launch_button.grid(row=0, column=0, padx=5, pady=5)

scan_button = Button(Action_Frame, text='Scan', command=scan)
scan_button.grid(row=1, column=0, padx=5, pady=5)

quit_button = Button(Action_Frame, text='Quit', command=main_window.destroy)
quit_button.grid(row=2, column=0, padx=5, pady=5)

# Show results
LbResult = Label(Result_Frame, textvariable=result)
LbResult.pack(side=LEFT, padx=5, pady=5)

main_window.mainloop()