import asyncio
import sys

import cozmo
from cozmo.util import degrees


async def turn_left(sdk_conn):
    robot = await sdk_conn.wait_for_robot()
    cozmo.logger.info("Turning robot 1")
    await robot.turn_in_place(degrees(90)).wait_for_completed()

async def turn_right(sdk_conn):
    robot = await sdk_conn.wait_for_robot()
    cozmo.logger.info("Turning robot 2")
    await robot.turn_in_place(degrees(-90)).wait_for_completed()


if __name__ == '__main__':
    cozmo.setup_basic_logging()
    loop = asyncio.get_event_loop()

    # Connect to both robots
    try:
        conn1 = cozmo.connect_on_loop(loop)
        conn2 = cozmo.connect_on_loop(loop)
    except cozmo.ConnectionError as e:
        sys.exit("A connection error occurred: %s" % e)

    # Run two independent coroutines concurrently, one on each connection
    task1 = asyncio.ensure_future(turn_left(conn1), loop=loop)
    task2 = asyncio.ensure_future(turn_right(conn2), loop=loop)

    # wait for both coroutines to complete before exiting the program
    loop.run_until_complete(asyncio.gather(task1, task2))
