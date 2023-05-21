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
        self.speed = {"x": [0], "y": [0], "z": [0]}
        self.acc = {"x": [0], "y": [0], "z": [0]}
        self.acc_ang = {"x": [0], "y": [0], "z": [0]}
        self.cur_velo_label, self.cur_acc_label, self.cur_acc_ang_label, self.cur_acc_ang_max_label = tk.Label(), tk.Label(), tk.Label(), tk.Label()
        self.cur_acc_ang = ''
        self.cur_acc = ''
        self.cur_velo = ''
        self.cur_acc_ang = None
        self.cur_acc_ang_max = None
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

            self.acc_ang["x"].append(random.randint(3, 20))
            self.acc_ang["y"].append(random.randint(3, 20))
            self.acc_ang["z"].append(random.randint(3, 20))
            
            # Add the new Positions to the Plot
            x = np.asarray(self.positions["x"])
            y = np.asarray(self.positions["y"])
            z = np.asarray(self.positions["z"])
            
            # Debugging
            #print(self.positions)
            
            # Update content of the plots

            self.ax2D.clear()
            self.ax3D.clear()
            self.ax2D.plot(x, y)
            self.ax2D.set_ylabel('X')
            self.ax2D.set_xlabel('Y')
            self.ax3D.plot(x, y, z)

            # Edit the text of the Labels
            self.cur_velo = "\tVelocity: \nx:\t"+ str(self.speed['x'][-1]) + '\ny:\t'+str(self.speed['y'][-1])+'\nz:\t'+str(self.speed['z'][-1])
            self.cur_acc = "\tAcceleration: \nx:\t"+ str(self.acc['x'][-1]) + '\ny:\t'+str(self.acc['y'][-1])+'\nz:\t'+str(self.acc['z'][-1])
            self.cur_acc_ang = "\tAngular Acceleration: \nx:\t"+ str(self.acc_ang['x'][-1]) + '\ny:\t'+str(self.acc_ang['y'][-1])+'\nz:\t'+str(self.acc_ang['z'][-1])
            self.cur_acc_ang_max = "\tMax Angular Acceleration: \nx:\t"+  str(max(self.acc_ang['x'])) + '\ny:\t'+str(max(self.acc_ang['y']))+'\nz:\t' + str(max(self.acc_ang['z']))

            self.label_frame.remove(self.cur_velo_label)
            self.cur_velo_label = tk.Label(text=self.cur_velo)
            self.label_frame.add(self.cur_velo_label)
            self.label_frame.remove(self.cur_acc_label)
            self.cur_acc_label = tk.Label(text=self.cur_acc)
            self.label_frame.add(self.cur_acc_label)
            self.label_frame.remove(self.cur_acc_ang_label)
            self.cur_acc_ang_label = tk.Label(text=self.cur_acc_ang)
            self.label_frame.add(self.cur_acc_ang_label)
            self.label_frame.remove(self.cur_acc_ang_max_label)
            self.cur_acc_ang_max_label = tk.Label(text=self.cur_acc_ang_max)
            self.label_frame.add(self.cur_acc_ang_max)


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

        # Starting the Data Column
        data_fig = plt.figure(figsize=plt.figaspect(2.))
        data_fig.suptitle('Current Data for Red Sparrow')

        # Plots

        # .....
        self.label_frame = tk.PanedWindow(orient="vertical")
        self.label_frame.grid(row=0, column=1) 
        self.canvas.draw()


root=tk.Tk()
root.geometry("800x900")
app=Application(master=root)
app.mainloop()