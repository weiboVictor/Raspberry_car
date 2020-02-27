from time import sleep
from redis import Redis

cli = Redis('localhost')

while True:
    print(int(cli.get('share_place')))
    sleep(1)