import time
import RPi.GPIO as GPIO
from redis import Redis

IR01 = 14
IR02 = 15
IR03 = 23

GPIO.setmode(GPIO.BCM)
GPIO.setup(IR01,GPIO.IN)
GPIO.setup(IR02,GPIO.IN)
GPIO.setup(IR03,GPIO.IN)
cli = Redis('localhost')

class InfraRed:
    def run(self):
        while True:
            time.sleep(0.02)
            self.LMR=0x00
            if GPIO.input(IR01)==True:
                self.LMR=(self.LMR | 4) # Left
            if GPIO.input(IR02)==True:
                self.LMR=(self.LMR | 2) # Middle
            if GPIO.input(IR03)==True:
                self.LMR=(self.LMR | 1) # Right
            
            cli.set('infrared_LMR', self.LMR)

infrared=InfraRed()
# Main program logic follows:
if __name__ == '__main__':
    print ('InfraRed is starting ... ')
    try:
        infrared.run()
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
        PWM.setMotorModel(0,0,0,0)
