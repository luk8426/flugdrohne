import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk  
import numpy as np
import threading as td
import time
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
        self.bat2d = None

        self.createWidgets()
        self.updateThread = td.Thread(target=self.readMavLinkAndUpdateGui)
        self.updateThread.start()     




    def readMavLinkAndUpdateGui(self):
        while(True):
            
            # Mock for new Input, we have to create a socket to the MAV-UDP here
            time.sleep(0.001)
            x = np.asarray(positions["x"])
            y = np.asarray(positions["y"])
            z = np.asarray(positions["z"])


            # Update content of the plots
            try:
                self.ax2D.clear()
                self.ax3D.clear()
                self.bat2d.clear()
                self.ax2D.plot(x, y)
                self.ax3D.plot(x, y, z)
                self.ax3D.set_ylabel('N')
                self.ax3D.set_xlabel('E')
                self.ax3D.set_zlabel('D')
                self.ax2D.set_ylabel('N')
                self.ax2D.set_xlabel('E')
                self.bat2d.plot(battery_values[1], battery_values_gradient[0])
                self.bat2d.set_ylabel('Avarage % Battery lost / s between 2 waypoints')
                self.bat2d.set_xlabel('Time')
            except:
                pass

            self.canvas.draw()




    
    def createWidgets(self):
        # Set up a figure twice as tall as it is wide
        fig_pos = plt.figure()#figsize=plt.figaspect(2.))
        fig_pos.suptitle('Red Sparrow Live Position and Battery')

        gs = plt.GridSpec(2, 2, figure=fig_pos)
        # First subplot
        self.ax2D = fig_pos.add_subplot(gs[1, 0])

        x = np.asarray(positions["x"])
        y = np.asarray(positions["y"])
        z = np.asarray(positions["z"])

        self.ax2D.plot(x, y)
        #self.ax2D.grid(True)


        # Second subplot
        self.ax3D = fig_pos.add_subplot(gs[1, 1], projection='3d')
        self.ax3D.plot(x, y, z)

        # Battery subplot
        self.bat2d = fig_pos.add_subplot(gs[0, :])
        self.bat2d.plot(battery_values[0], battery_values[1])

        # This is for the GUI
        self.canvas=FigureCanvasTkAgg(fig_pos,master=root)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH,expand=True)

        # Starting the Data Column
        
        
        self.canvas.draw()

async def run():
    drone = System(mavsdk_server_address="localhost")
    await drone.connect(system_address="udp://:14540")
    #asyncio.ensure_future(updateMissionStatus(drone))
    asyncio.ensure_future(updateVeloPosition(drone))
    asyncio.ensure_future(updateBattery(drone))
    #asyncio.ensure_future(updateHeading(drone))
    while True:
        await asyncio.sleep(1)

def missionChecker():
    global bat_val_cnt
    global idx_bat_val
    global nextWaypoint
    if (nextWaypoint):
        print("New Waypoint")
        nextWaypoint = False
        idx_bat_val += bat_val_cnt
        bat_val_cnt = 0

async def updateHeading(drone):
    async for heading in drone.telemetry.heading():
        global heading_changing
        global headings
        global nextWaypoint
        headings.append(heading.heading_deg)
        #print(headings)
        if(len(headings)<8):
            continue
        if (abs(headings[-1]-headings[-3])>8):
            print("In Here")
            if (not heading_changing):
                print("Changing")
                heading_changing = True
                nextWaypoint = True
        else:
            heading_changing = False
        
async def updateVeloPosition(drone):
    async for posvelo in drone.telemetry.position_velocity_ned():
        global nextWaypoint
        speed["vertical"].append(posvelo.velocity.down_m_s)
        if((abs(speed["vertical"][-1])<=0.5) & (abs(speed["vertical"][-2])>0.5) |
           (abs(speed["vertical"][-1])<=2.5) & (abs(speed["vertical"][-2])>2.5) |
           (abs(speed["vertical"][-1])>=0.5) & (abs(speed["vertical"][-2])<0.5) |
           (abs(speed["vertical"][-1])>=2.5) & (abs(speed["vertical"][-2])<2.5)):
            nextWaypoint = True
        speed["horizontal"].append(math.sqrt(posvelo.velocity.north_m_s**2 + posvelo.velocity.east_m_s**2))
        if (abs(speed["horizontal"][-1])<=2) & (abs(speed["horizontal"][-2])>2):
            nextWaypoint = True
        positions["z"].append(posvelo.position.down_m)
        positions["x"].append(posvelo.position.north_m)
        positions["y"].append(posvelo.position.east_m)

async def updateMissionStatus(drone):
    async for mission_progress in drone.mission.mission_progress():
        print(mission_progress.current)

async def updateBattery(drone):
    async for battery in drone.telemetry.battery():
        global battery_values
        global battery_values_gradient
        global bat_val_cnt
        bat_val_cnt+=1
        missionChecker()
        battery_values = np.hstack((battery_values, [[1-battery.remaining_percent],[time.time()-start_time]]))
        battery_values_gradient = np.hstack((battery_values_gradient, [[0],[time.time()-start_time]]))
        if(bat_val_cnt>2):
            battery_values_gradient[0][idx_bat_val:idx_bat_val+bat_val_cnt] = sum(np.gradient(battery_values[0][idx_bat_val:idx_bat_val+bat_val_cnt], battery_values[1][idx_bat_val:idx_bat_val+bat_val_cnt]))/bat_val_cnt
        #print(battery_values)

headings = [0]
heading_changing = False
nextWaypoint = False
start_time = time.time()
bat_val_cnt = 0
idx_bat_val = 0
speed = {"vertical": [0], "horizontal": [0]}
acc = {"vertical": [0], "total": [0]}
speed_ang = {"x": [0], "y": [0], "z": [0]}
acc_ang = {"x": [0], "y": [0], "z": [0]}
imu_timestamps = [0]
positions = {"x": [], "y": [], "z": []} # NorthEastDown
battery_values = np.array([[],[]])
battery_values_gradient = np.array([[],[]])
mavlinkThread = td.Thread(target=asyncio.run, args=[run()])
mavlinkThread.start()
root=tk.Tk()
root.geometry("1000x900")
root.configure(background='#b50d0d')
app=Application(master=root)
app.mainloop()
