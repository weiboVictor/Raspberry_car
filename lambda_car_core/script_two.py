from time import sleep
from redis import Redis

cli = Redis('localhost')

while True:
    print(int(cli.get('ultrasonic_R')))
    print(int(cli.get('ultrasonic_M')))
    print(int(cli.get('ultrasonic_L')))
    sleep(0.2)