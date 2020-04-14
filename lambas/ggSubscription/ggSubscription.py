import json
import logging
import sys
import os
from redis import Redis
#configuration
THIS_CAR = os.environ['car_name']
TOPIC = "broadcast_traffic"

# Setup logging to stdout
logger = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


def lambda_handler(event, context):
    # TODO implement
    logging.debug(event)
    if event["type"] == "traffic" and event["reporter"] != THIS_CAR:
        logging.debug("Add to redis traffic table")
        cli = Redis('localhost')
        cli.rpush("broadcast_traffic", event)
    else:
        logging.debug("type is %s, reporter is %s ignored."%(event["type"], event["reporter"]))
