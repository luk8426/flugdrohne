#!/usr/bin/env python3

import asyncio
from mavsdk import System
import mavsdk


async def run():
    # Init the drone
    drone = System()
    await drone.connect(system_address="udp://:14540")


    # Start the tasks
    #asyncio.ensure_future(print_battery(drone))
    #asyncio.ensure_future(print_gps_info(drone))
    #asyncio.ensure_future(print_in_air(drone))
    #asyncio.ensure_future(print_position(drone))
    asyncio.ensure_future(print_pwm_out(drone))

    while True:
        await asyncio.sleep(1)


async def print_battery(drone):
    async for battery in drone.telemetry.battery():
        print(f"Battery: {battery.remaining_percent}")


async def print_gps_info(drone):
    async for gps_info in drone.telemetry.gps_info():
        print(f"GPS info: {gps_info}")


async def print_in_air(drone):
    async for in_air in drone.telemetry.in_air():
        print(f"In air: {in_air}")


async def print_position(drone):
    async for position in drone.telemetry.position():
        print(position)


async def print_pwm_out(drone):
    async for actuator_control_target in drone.telemetry.actuator_control_target():
        print(actuator_control_target)


if __name__ == "__main__":
    # Start the main function
    asyncio.run(run())
