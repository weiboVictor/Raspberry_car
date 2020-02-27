from redis import Redis
from time import sleep

cli = Redis('localhost')
shared_var = 1

while True:
   cli.set('share_place', shared_var)
   shared_var += 1
   sleep(1)