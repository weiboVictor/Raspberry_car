import time
def wait_for_echo(timeout):
        count = timeout
        while count>0:
            count = count-1

start = time.time()
wait_for_echo(10000)
finish = time.time()

pulse_len = finish-start
distance_cm = pulse_len/0.000058

print(pulse_len)
print(distance_cm)