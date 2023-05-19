import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk  
import numpy as np
import threading as td
from time import sleep
import random


class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self,master)
        self.canvas = None
        self.ax3D = None
        self.ax2D = None
        self.positions = {"x": [0], "y": [0], "z": [0]}
        self.createWidgets()
        self.updateThread = td.Thread(target=self.readMavLinkAndUpdateGui)
        self.updateThread.start()


    def readMavLinkAndUpdateGui(self):
        while(True):
            
            # Mock for new Input, we have to create a socket to the MAV-UDP here
            sleep(3)
            self.positions["x"].append(random.randint(3, 20))
            self.positions["y"].append(random.randint(3, 20))
            self.positions["z"].append(random.randint(3, 20))
            x = np.asarray(self.positions["x"])
            y = np.asarray(self.positions["y"])
            z = np.asarray(self.positions["z"])
            # Debugging
            #print(self.positions)
            self.ax2D.clear()
            self.ax3D.clear()
            self.ax2D.plot(x, y)
            self.ax2D.set_ylabel('X')
            self.ax2D.set_xlabel('Y')
            self.ax3D.plot(x, y, z)
            self.canvas.draw()




    
    def createWidgets(self):
        # Set up a figure twice as tall as it is wide
        fig = plt.figure(figsize=plt.figaspect(2.))
        fig.suptitle('Red Sparrow Live-Telemetry')

        # First subplot
        self.ax2D = fig.add_subplot(2, 1, 1)

        x = np.asarray(self.positions["x"])
        y = np.asarray(self.positions["y"])
        z = np.asarray(self.positions["z"])

        self.ax2D.plot(x, y)
        #self.ax2D.grid(True)
        self.ax2D.set_ylabel('X')
        self.ax2D.set_xlabel('Y')

        # Second subplot
        self.ax3D = fig.add_subplot(2, 1, 2, projection='3d')
        self.ax3D.plot(x, y, z)

        # This is for the GUI
        self.canvas=FigureCanvasTkAgg(fig,master=root)
        self.canvas.get_tk_widget().grid(row=0,column=0)
        self.canvas.draw()


root=tk.Tk()
root.geometry("800x900")
app=Application(master=root)
app.mainloop()