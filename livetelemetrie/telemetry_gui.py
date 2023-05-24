import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk  
import numpy as np
import threading as td
from time import sleep
import random

import asyncio
from mavsdk import System


class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self,master)
        self.canvas = None
        self.ax3D = None
        self.ax2D = None
        self.speed = {"x": [0], "y": [0], "z": [0]}
        self.acc = {"x": [0], "y": [0], "z": [0]}
        self.acc_ang = {"x": [0], "y": [0], "z": [0]}
        #self.positions = {"x": [0], "y": [0], "z": [0]}
        self.cur_velo_label, self.cur_acc_label, self.cur_acc_ang_label, self.cur_acc_ang_max_label = tk.Label(), tk.Label(), tk.Label(), tk.Label()
        self.pwm_labels = [tk.Label() for i in range(5)]
        self.pwm_values = [0 for i in range(5)]
        self.cur_acc_ang = ''
        self.cur_acc = ''
        self.cur_velo = ''
        self.cur_acc_ang = None
        self.cur_acc_ang_max = None
        self.createWidgets()
        self.updateThread = td.Thread(target=self.readMavLinkAndUpdateGui)
        self.updateThread.start()     




    def readMavLinkAndUpdateGui(self):
        while(True):
            
            # Mock for new Input, we have to create a socket to the MAV-UDP here
            sleep(1)

            # Update the Positions

            #self.positions["x"].append(random.randint(3, 20))
            #self.positions["y"].append(random.randint(3, 20))
            #self.positions["z"].append(random.randint(3, 20))
            x = np.asarray(positions["x"])
            y = np.asarray(positions["y"])
            z = np.asarray(positions["z"])

            # Update the speed/acc values
            #self.acc_ang["x"].append(random.randint(3, 20))
            #self.acc_ang["y"].append(random.randint(3, 20))
            #self.acc_ang["z"].append(random.randint(3, 20))
            
            # Update the PWM values
            #self.pwm_values = [random.randint(900, 2200) for i in range(5)]

            # Debugging
            #print(self.positions)

            # Update the text of the Speed/Acc Labels
            self.cur_velo = "Velocity: \nx:\t"+ str(self.speed['x'][-1]) + '\ny:\t'+str(self.speed['y'][-1])+'\nz:\t'+str(self.speed['z'][-1])
            self.cur_acc = "Acceleration: \nx:\t"+ str(self.acc['x'][-1]) + '\ny:\t'+str(self.acc['y'][-1])+'\nz:\t'+str(self.acc['z'][-1])
            self.cur_acc_ang = "Angular Acceleration: \nx:\t"+ str(self.acc_ang['x'][-1]) + '\ny:\t'+str(self.acc_ang['y'][-1])+'\nz:\t'+str(self.acc_ang['z'][-1])
            self.cur_acc_ang_max = "Max Angular Acceleration: \nx:\t"+  str(max(self.acc_ang['x'])) + '\ny:\t'+str(max(self.acc_ang['y']))+'\nz:\t' + str(max(self.acc_ang['z']))

            # Update the text for PWM Output Labels
            # n.a

            # Update content of the plots

            self.ax2D.clear()
            self.ax3D.clear()
            self.ax2D.plot(x, y)
            self.ax2D.set_ylabel('X')
            self.ax2D.set_xlabel('Y')
            self.ax3D.plot(x, y, z)

            # Update the labels

            for i in range(5):
                self.pwm_label_frame.remove(self.pwm_labels[i])
                self.pwm_labels[i] = tk.Label(anchor='w', background='#b50d0d', foreground='white', text='Actuator ' + str(i+1)+ ' Output:\t' + str(self.pwm_values[i]) + ' us')
                self.pwm_label_frame.add(self.pwm_labels[i])
            self.label_frame.remove(self.cur_velo_label)
            self.cur_velo_label = tk.Label(text=self.cur_velo, anchor='w', background='#b50d0d', foreground='white')
            self.label_frame.add(self.cur_velo_label)
            self.label_frame.remove(self.cur_acc_label)
            self.cur_acc_label = tk.Label(text=self.cur_acc, anchor='w', background='#b50d0d', foreground='white')
            self.label_frame.add(self.cur_acc_label)
            self.label_frame.remove(self.cur_acc_ang_label)
            self.cur_acc_ang_label = tk.Label(text=self.cur_acc_ang, anchor='w', background='#b50d0d', foreground='white')
            self.label_frame.add(self.cur_acc_ang_label)
            self.label_frame.remove(self.cur_acc_ang_max_label)
            self.cur_acc_ang_max_label = tk.Label(text=self.cur_acc_ang_max, anchor='w', background='#b50d0d', foreground='white')
            self.label_frame.add(self.cur_acc_ang_max_label)
            self.canvas.draw()




    
    def createWidgets(self):
        # Set up a figure twice as tall as it is wide
        fig = plt.figure(figsize=plt.figaspect(2.))
        fig.suptitle('Red Sparrow Live-Telemetry')

        # First subplot
        self.ax2D = fig.add_subplot(2, 1, 1)

        x = np.asarray(positions["x"])
        y = np.asarray(positions["y"])
        z = np.asarray(positions["z"])

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
        self.label_frame.configure(background='white')
        self.label_frame.grid(row=0, column=1) 
        self.pwm_label_frame = tk.PanedWindow(orient="vertical")
        self.pwm_label_frame.configure(background='white')
        self.pwm_label_frame.grid(row=0, column=2)
        self.canvas.draw()

async def run():
# Init the drone
    drone = System()
    await drone.connect(system_address="udp://:14540")
    asyncio.ensure_future(updatePosition(drone))
    #asyncio.ensure_future(print_in_air(drone))#, app))
    while True:
        await asyncio.sleep(1)

async def updatePosition(drone):
    async for position in drone.telemetry.position():
        positions["z"].append(position.relative_altitude_m)
        positions["x"].append(abs(position.longitude_deg))
        positions["y"].append(abs(position.latitude_deg)) 

async def print_in_air(drone):
    async for in_air in drone.telemetry.in_air():
        print(f"In air: {in_air}")

#positions = {"x": [8550], "y": [47400], "z": [0]}
positions = {"x": [], "y": [], "z": []}
mavlinkThread = td.Thread(target=asyncio.run, args=[run()])
mavlinkThread.start()
root=tk.Tk()
root.geometry("1000x900")
root.configure(background='white')
app=Application(master=root)
app.mainloop()
