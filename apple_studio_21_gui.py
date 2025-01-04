#! /usr/bin/env python

from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showinfo
import subprocess

window = Tk()
window.title("USB Control for Apple Studio Display")
window.tk.call('tk', 'scaling', 1)
window.configure(padx=8, pady=8)
window.resizable(False, False)

vcp_codes = {
    "0x10": "Brightness",
    "0x12": "Contrast",
    "0x20": "H Phase",
    "0x22": "H Size",
    "0x30": "V Phase",
    "0x32": "V Size",
    "0x24": "H Pin",
    "0x42": "H Keystone",
    "0x40": "H Key Balance",
    "0x44": "Rotation",
    "0x28": "H Stat conv",
    "0x38": "V Stat conv",
}

def get_parameter(param_code):
    return subprocess.run(["sudo", "usbmonctl", "-g", "F,"+str(param_code)], capture_output=True, text=True).stdout.split(" ")[0]

class Slider_box():
    def __init__(self, parent, param, index):
        self.parent = parent
        self.param = param
        self.index = index

    def new_sliderbox(self):
        self.value = IntVar(value=get_parameter(self.param))
        self.label = ttk.Label(self.parent, text=vcp_codes[self.param])

        def field_entered(event):
            newentry = self.value.get()
            if int(newentry) > 255:
                self.slider.set(255)
            else:
                self.slider.set(int(newentry))

        def slider_changed(value):
            self.value.set(int(float(value)))
            subprocess.run(["sudo", "usbmonctl", "-s", "F,"+str(self.param)+"="+str(value)])
        
        def buttondown():
            self.downone.state(["disabled"])
            minusone = self.slider.get()-1
            self.slider.set(minusone)
            self.downone.state(["!disabled"])

        def buttonup():
            self.upone.state(["disabled"])
            plusone = self.slider.get()+1
            self.slider.set(plusone)
            self.upone.state(["!disabled"])

        self.slidervalue = ttk.Entry(self.parent, width=4, justify=CENTER, textvariable=self.value)
        self.slidervalue.bind("<Return>", field_entered)

        self.slider = ttk.Scale(self.parent, from_=0, to=255, length=320, command=slider_changed)
        self.downone = ttk.Button(self.parent,  width=4, text="<", command=buttondown)
        self.upone = ttk.Button(self.parent, width=4, text=">", command=buttonup)

        self.slider.set(get_parameter(self.param))
        
        self.slider.grid(row=self.index, column=1, padx=4)
        self.downone.grid(row=self.index, column=2, padx=2, pady=2)
        self.slidervalue.grid(row=self.index, column=3, padx=4)
        self.upone.grid(row=self.index, column=4, padx=2, pady=2)
        self.label.grid(sticky=W)

freq = ttk.Label(window, text="Horizontal: "+str(int(subprocess.run(["sudo", "usbmonctl", "-g", "F,0xac"], capture_output=True, text=True).stdout.split(" ")[0])/1000)+"kHz Vertical: "+str(int(subprocess.run(["sudo", "usbmonctl", "-g", "F,0xae"], capture_output=True, text=True).stdout.split(" ")[0])/100)+"Hz") 
freq.pack(expand=True)

main_frame = ttk.Frame(window, padding=4, borderwidth=3)
main_frame.pack(expand=True)
main_frame.columnconfigure(0, weight=1)
main_frame.columnconfigure(1, weight=1)
main_frame.columnconfigure(2, weight=1)
main_frame.columnconfigure(3, weight=1)
main_frame.columnconfigure(4, weight=1)
sliderindex = 0
for param_code in vcp_codes.keys():
    slider = Slider_box(main_frame, param_code, sliderindex)
    slider.new_sliderbox()
    sliderindex += 1

def donger():
            print("dong")
            subprocess.run(["sudo", "usbmonctl", "-s", "F,0x01,0,0=1"])
            showinfo(title='Notice',message='Dong !')
def saver():
            print("saved")
            subprocess.run(["sudo", "usbmonctl", "-s", "F,0xb0,0,0=1"])
            showinfo(title='Notice',message='Settings saved')

savebutton = ttk.Button(main_frame, text="Save settings", command=saver)
savebutton.grid(row=sliderindex+1, column=2, columnspan=3, padx=3, pady=12, sticky=EW)
dongbutton = ttk.Button(main_frame, text="Degauss", command=donger)
dongbutton.grid(row=sliderindex+2, column=2, columnspan=3, padx=3, pady=2, sticky=EW)

window.mainloop()
