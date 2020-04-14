#
# Copyright 2010-2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#

# greengrassHelloWorld.py
# Demonstrates a simple publish to a topic using Greengrass core sdk
# This lambda function will retrieve underlying platform information and send
# a hello world message along with the platform information to the topic
# 'hello/world'. The function will sleep for five seconds, then repeat.
# Since the function is long-lived it will run forever when deployed to a
# Greengrass core.  The handler will NOT be invoked in our example since
# the we are executing an infinite loop.

import logging
import platform
import sys
import os
from threading import Timer
from redis import Redis
import greengrasssdk
import json
import time

#Configuration
TOPIC = os.environ['topic'] #"car1/sensors"
FREQUENCY = int(os.environ['frequency']) # 5

# Setup logging to stdout
logger = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

# Creating a greengrass core sdk client
client = greengrasssdk.client("iot-data")

my_platform = platform.platform()


def upload_to_cloud():
    try:
        cli = Redis('localhost')
        ultrasonic_M = int(cli.get('ultrasonic_M'))
        infrared_LMR = int(cli.get('infrared_LMR'))
        #battery_level = int(cli.get('battery_level'))
        #motor_1 = int(cli.get('motor_1'))
        #motor_2 = int(cli.get('motor_2'))
        #motor_3 = int(cli.get('motor_3'))
        #motor_4 = int(cli.get('motor_4'))
        #rfid_pos = int(cli.get('rfid_pos'))
        #accelerator_x = int(cli.get('accelerator_x'))
        #accelerator_y = int(cli.get('accelerator_y'))
        #accelerator_z = int(cli.get('accelerator_z'))

        MSG=json.dumps({"ultrasonic_M": ultrasonic_M,"infrared_LMR": infrared_LMR, "local_time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())})
    except Exception as e:
        logger.error("Failed to include redis: " + repr(e))

    try:
        client.publish(
            topic=TOPIC, queueFullPolicy="AllOrException", payload=MSG
        )
        
    except Exception as e:
        logger.error("Failed to publish message: " + repr(e))

    # Asynchronously schedule this function to be run again in 5 seconds
    Timer(FREQUENCY, upload_to_cloud).start()


# Start executing the function above
upload_to_cloud()


# This is a dummy handler and will not be invoked
# Instead the code above will be executed in an infinite loop for our example
def function_handler(event, context):
    return
