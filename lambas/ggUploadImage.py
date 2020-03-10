import logging
import sys
from redis import Redis
from botocore.exceptions import ClientError
import json
import time
from threading import Timer
import boto3
import uuid
import os
# Setup logging to stdout
logger = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

DYNAMO_DB = "Raspberry_Car_Object"
S3_BUCKET = "iot-raspberry-car"
S3_KEY = "camera_images/"


def s3_upload(img_local_path):
    try:
        logging.debug("s3_upload: entry")
        file_name = os.path.basename(img_local_path)
        s3 =boto3.resource('s3')
        logging.debug("s3_upload: client loaded.")
        s3.meta.client.upload_file(img_local_path, S3_BUCKET, S3_KEY+file_name)
        #s3_client.upload_file(img_local_path, S3_BUCKET, S3_KEY+file_name)
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
            item = cli.lpop('car')
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
                    logging.debug("dynamodb: entry")
                    dynamodb_client = boto3.client('dynamodb')
                    dynamodb_client.put_item(TableName=DYNAMO_DB, 
                                Item={'detection_time': {'S':detection_time}, 
                                    'position':{'S': position},
                                    'rfid_pos':{'S': rfid_pos},
                                    's3_path':{'S': S3_KEY+file_name},
                                    'hash_tag':{'S': uniqueid} }) 
                    logging.debug("dynamodb: success")
                except ClientError as e:
                    logger.error(e)

    except Exception as e:
        logger.error("upload_img_to_cloud error: " + repr(e))

    # Asynchronously schedule this function to be run again in 5 seconds
    Timer(10, upload_img_to_cloud).start()


# Start executing the function above
upload_img_to_cloud()


# This is a dummy handler and will not be invoked
# Instead the code above will be executed in an infinite loop for our example
def function_handler(event, context):
    return
