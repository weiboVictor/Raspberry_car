import logging
import sys
from redis import Redis
from botocore.exceptions import ClientError
import json
import greengrasssdk
import time
from threading import Timer
import boto3
import uuid
import os
#Configuration while setup lambda in Greengrass
#DYNAMO_DB = "Raspberry_Car_Object"
S3_BUCKET = os.environ['s3_bucket'] #iot-raspberry-car
S3_KEY = os.environ['s3_key'] #car1/camera_images/
CAR = os.environ['car_name'] # car1
TOPIC = os.environ['topic'] # broadcast/traffic/objects
FREQUENCY = int(os.environ['frequency'])
EVENT_TYPE = "traffic"

# Setup logging to stdout
logger = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

client = greengrasssdk.client("iot-data")

def s3_upload(img_local_path):
    try:
        logging.debug("s3_upload: entry")
        file_name = os.path.basename(img_local_path)
        s3_client = boto3.client('s3')
        s3_client.upload_file(img_local_path, S3_BUCKET, S3_KEY+file_name)
        logging.debug("s3_upload: success: ")
        logging.debug("s3_upload: %s"%img_local_path)
        logging.debug("s3_upload: %s"%S3_BUCKET)
        logging.debug("s3_upload: %s"%file_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True


def upload_img_to_cloud():
    try:
        cli = Redis('localhost')
        while True:
            item = cli.lpop('car_images')
            if not item:
                logger.info("car queue is empty")
                break
            dt = json.loads(item)
            img_local_path = str(dt['img_local_path'])
            detection_time = str(dt['detection_time'])
            position = str(dt['position'])
            rfid_pos = str(dt['rfid_pos'])
            logging.debug("redis data is below: ")
            logging.debug(dt)
            if s3_upload(img_local_path):
                uniqueid = uuid.uuid4().hex
                file_name = os.path.basename(img_local_path)
                try:
                    logging.debug("mqtt: entry")
                    MSG=json.dumps({"type":EVENT_TYPE,"reporter":CAR,"position": position,"rfid_pos": rfid_pos, "object_s3_path":S3_KEY+file_name, "hash_tag": uniqueid,"detection_time": detection_time})
                    client.publish(
                        topic=TOPIC, queueFullPolicy="AllOrException", payload=MSG
                    )
                except Exception as e:
                    logger.error(e)

    except Exception as e:
        logger.error("upload_img_to_cloud error: " + repr(e))

    # Asynchronously schedule this function to be run again in 5 seconds
    Timer(FREQUENCY, upload_img_to_cloud).start()


# Start executing the function above
upload_img_to_cloud()


# This is a dummy handler and will not be invoked
# Instead the code above will be executed in an infinite loop for our example
def function_handler(event, context):
    return
