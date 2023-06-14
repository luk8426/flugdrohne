import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk  
import numpy as np
import threading as td
from time import sleep
import random

import math
import asyncio
from mavsdk import System


class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self,master)
        self.canvas = None
        self.ax3D = None
        self.ax2D = None
        self.cur_velo_label, self.cur_acc_label, self.cur_acc_ang_label, self.cur_acc_ang_max_label = tk.Label(), tk.Label(), tk.Label(), tk.Label()
        self.pwm_labels = [tk.Label() for i in range(5)]
        self.battery_label = tk.Label()
        self.cur_acc_ang = ''
        self.cur_acc = ''
        self.cur_velo = ''
        self.battery_text = ""
        self.cur_acc_ang = None
        self.cur_acc_ang_max = None
        self.createWidgets()
        self.updateThread = td.Thread(target=self.readMavLinkAndUpdateGui)
        self.updateThread.start()     




    def readMavLinkAndUpdateGui(self):
        while(True):
            
            # Mock for new Input, we have to create a socket to the MAV-UDP here
            sleep(0.001)
            x = np.asarray(positions["x"])
            y = np.asarray(positions["y"])
            z = np.asarray(positions["z"])

            # Update the text of the Speed/Acc Labels
            self.cur_velo = "Velocity: \nHorizontal:\t%.2f\nVertical:\t\t%.2f" % (speed['horizontal'][-1], speed['vertical'][-1])
            self.cur_acc = "Acceleration: \nTotal:\t\t%.2f\nVertical:\t\t%.2f" % (acc['total'][-1], acc['vertical'][-1])
            self.cur_acc_ang = "Angular Acceleration: \nx:\t\t%.5f\ny:\t\t%.5f\nz:\t\t%.5f" % (acc_ang['x'][-1], acc_ang['y'][-1], acc_ang['z'][-1])
            self.cur_acc_ang_max = "Max Angular Acceleration: \nx:\t\t%.2f\ny:\t\t%.2f\nz:\t\t%.2f" % (max([abs(x) for x in acc_ang['x']]), max([abs(y) for y in acc_ang['y']]), max([abs(z) for z in acc_ang['z']]))
            self.battery_text = ("Battery Status: \t %.1f " % (battery_value*100)) + "%"

            # Update the text for PWM Output Labels
            # n.a

            # Update content of the plots
            try:
                self.ax2D.clear()
                self.ax3D.clear()
                self.ax2D.plot(x, y)
                self.ax2D.set_ylabel('N')
                self.ax2D.set_xlabel('E')
                self.ax3D.plot(x, y, z)
            except:
                pass

            # Update the labels

            for i in range(5):
                self.pwm_label_frame.remove(self.pwm_labels[i])
                self.pwm_labels[i] = tk.Label(anchor='w', background='#b50d0d', foreground='white', text='Actuator ' + str(i+1)+ ' Output:\t' + str(pwm_values[i]) + ' us')
                self.pwm_label_frame.add(self.pwm_labels[i])
            self.label_frame.remove(self.cur_velo_label)
            self.cur_velo_label = tk.Label(text=self.cur_velo, anchor='w', background='#b50d0d', foreground='white', justify=tk.LEFT)
            self.label_frame.add(self.cur_velo_label)
            self.label_frame.remove(self.cur_acc_label)
            self.cur_acc_label = tk.Label(text=self.cur_acc, anchor='w', background='#b50d0d', foreground='white', justify=tk.LEFT)
            self.label_frame.add(self.cur_acc_label)
            self.label_frame.remove(self.cur_acc_ang_label)
            self.cur_acc_ang_label = tk.Label(text=self.cur_acc_ang, anchor='w', background='#b50d0d', foreground='white', justify=tk.LEFT)
            self.label_frame.add(self.cur_acc_ang_label)
            self.label_frame.remove(self.cur_acc_ang_max_label)
            self.cur_acc_ang_max_label = tk.Label(text=self.cur_acc_ang_max, anchor='w', background='#b50d0d', foreground='white', justify=tk.LEFT)
            self.label_frame.add(self.cur_acc_ang_max_label)
            
            self.label_frame.remove(self.battery_label)
            self.battery_label = tk.Label(text=self.battery_text, anchor='w', background='#b50d0d', foreground='white', justify=tk.LEFT)
            self.label_frame.add(self.battery_label)

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
        self.label_frame = tk.PanedWindow(orient="vertical")
        self.label_frame.configure(background='#b50d0d')
        self.label_frame.grid(row=0, column=1) 
        self.pwm_label_frame = tk.PanedWindow(orient="vertical")
        self.pwm_label_frame.configure(background='#b50d0d')
        self.pwm_label_frame.grid(row=0, column=2)
        self.canvas.draw()

async def run():
    drone = System()
    await drone.connect(system_address="udp://:14540")
    asyncio.ensure_future(updateAccSpeedAng(drone))
    asyncio.ensure_future(updateVeloPosition(drone))
    asyncio.ensure_future(updatePWM(drone))
    asyncio.ensure_future(updateBattery(drone))
    while True:
        await asyncio.sleep(1)

async def updateGlobalPosition(drone):
    async for position in drone.telemetry.position():
        positions["z"].append(position.relative_altitude_m)
        positions["x"].append(abs(position.longitude_deg))
        positions["y"].append(abs(position.latitude_deg)) 

async def updateVeloPosition(drone):
    async for posvelo in drone.telemetry.position_velocity_ned ():
        speed["vertical"].append(posvelo.velocity.down_m_s)
        speed["horizontal"].append(math.sqrt(posvelo.velocity.north_m_s**2 + posvelo.velocity.east_m_s**2))
        positions["z"].append(posvelo.position.down_m)
        positions["x"].append(posvelo.position.north_m)
        positions["y"].append(posvelo.position.east_m)

async def updateAccSpeedAng(drone):
    async for imu in drone.telemetry.imu():
        new_acc = imu.acceleration_frd 
        acc["vertical"].append(new_acc.down_m_s2)
        acc["total"].append(math.sqrt(new_acc.forward_m_s2 **2 + new_acc.right_m_s2 **2 + new_acc.down_m_s2**2))
        new_ang_speed = imu.angular_velocity_frd
        speed_ang["x"].append(new_ang_speed.forward_rad_s)
        speed_ang["y"].append(new_ang_speed.right_rad_s)
        speed_ang["z"].append(new_ang_speed.down_rad_s)
        d_t = (imu.timestamp_us-imu_timestamps[-1])/1000000 # in s
        imu_timestamps.append(imu.timestamp_us)
        #if (len(imu_timestamps)!=1):
        acc_ang["x"].append((speed_ang["x"][-1]-speed_ang["x"][-2])/d_t)
        acc_ang["y"].append((speed_ang["y"][-1]-speed_ang["y"][-2])/d_t)
        acc_ang["z"].append((speed_ang["z"][-1]-speed_ang["z"][-2])/d_t)            

async def updatePWM(drone):
    async for actuator_output_status in drone.telemetry.actuator_output_status():
        global pwm_values
        pwm_values = actuator_output_status.actuator[0:4]

async def updateSpeedAng(drone):
    async for speed_ang in drone.telemetry.velocity_ned():
        acc["vertical"].append(acc.down_m_s2)
        acc["total"].append(math.sqrt(acc.forward_m_s2 **2 + acc.right_m_s2 **2 + acc.down_m_s2))

async def updateBattery(drone):
    async for battery in drone.telemetry.battery():
        global battery_value
        battery_value = battery.remaining_percent

async def print_in_air(drone):
    async for in_air in drone.telemetry.in_air():
        print(f"In air: {in_air}")

pwm_values = [0 for i in range(5)]
speed = {"vertical": [0], "horizontal": [0]}
acc = {"vertical": [0], "total": [0]}
speed_ang = {"x": [0], "y": [0], "z": [0]}
acc_ang = {"x": [0], "y": [0], "z": [0]}
imu_timestamps = [0]
positions = {"x": [], "y": [], "z": []} # NorthEastDown
battery_value = 0
mavlinkThread = td.Thread(target=asyncio.run, args=[run()])
mavlinkThread.start()
root=tk.Tk()
root.geometry("1000x900")
root.configure(background='#b50d0d')
app=Application(master=root)
app.mainloop()
