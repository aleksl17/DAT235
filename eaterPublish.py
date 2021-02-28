import paho.mqtt.publish as publish
import paho.mqtt.subscribe as subscribe
import tkinter as tk
import sys
import time

ipConnect = "10.0.0.201"


# ~ def key(event)
    # ~ if event.keysym == "Escape":
        # ~ root.destroy()
    # ~ if event.keysym == "Up":
        # ~ publish.single("dat235/groupnine/start", order, hostname=ipConnect)
        
def start(order):
    publish.single("dat235/groupnine/start", order, hostname=ipConnect)
    # ~ order = subscribe.simple("dat235/groupnine/start/#", hostname=ipConnect)
    # ~ print(order.payload)
    return


def up():
    publish.single("dat235/groupnine/joystick/up", hostname=ipConnect)
    # ~ msg = subscribe.simple("dat235/groupnine/start/#", hostname=ipConnect)
    # ~ print(msg.payload)
    return


def down():
    publish.single("dat235/groupnine/joystick/down", hostname=ipConnect)
    # ~ msg = subscribe.simple("dat235/groupnine/start/#", hostname=ipConnect)
    # ~ print(msg.payload)
    return


def left():
    publish.single("dat235/groupnine/joystick/left", hostname=ipConnect)
    # ~ msg = subscribe.simple("dat235/groupnine/start/#", hostname=ipConnect)
    # ~ print(msg.payload)
    return


def right():
    publish.single("dat235/groupnine/joystick/right", hostname=ipConnect)
    # ~ msg = subscribe.simple("dat235/groupnine/start/#", hostname=ipConnect)
    # ~ print(msg.payload)
    return

def stoplog():
    publish.single("dat235/groupnine/joystick/stoplog", hostname=ipConnect)
    
    #Load i python3: 'from eaterpublish import *'
    

class Example(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, width=100,  height=100)

        self.label = tk.Label(self, text="last key pressed:  ", width=20)
        self.label.pack(fill="both", padx=50, pady=50)

        self.label.bind("<w>", self.on_wasd)
        self.label.bind("<a>", self.on_wasd)
        self.label.bind("<s>", self.on_wasd)
        self.label.bind("<d>", self.on_wasd)
        self.label.bind("<q>", self.on_wasd)

        # give keyboard focus to the label by default, and whenever
        # the user clicks on it
        self.label.focus_set()
        self.label.bind("<1>", lambda event: self.label.focus_set())

    def on_wasd(self, event):
        self.label.configure(text="last key pressed: " + event.keysym)
        if event.keysym == "w":
            up()
            
        if event.keysym == "d":
            right()
            
        if event.keysym == "a":
            left()
            
        if event.keysym == "s":
            down()

        if event.keysym == "q":
            stoplog()


if __name__ == "__main__":
    root = tk.Tk()
    Example(root).pack(fill="both", expand=True)
    root.mainloop()
