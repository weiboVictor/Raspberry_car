from Ultrasonic import *
from servo import *
from redis import Redis

def run():
    pwm_S=Servo()
    pwm_S.setServoPwm('0',SERVO_ORIZON)
    pwm_S.setServoPwm('1',SERVO_VERTIC)
    ultrasonic=Ultrasonic()
    cli = Redis('localhost')

    while True:
        M = ultrasonic.get_distance()
        cli.set('ultrasonic_M', M)
        time.sleep(0.2)
        """
        pwm_S.setServoPwm('0',SERVO_ORIZON-30)
        L = self.get_distance()
        cli.set('ultrasonic_L', L)
        time.sleep(0.2)

        pwm_S.setServoPwm('0',SERVO_ORIZON)
        M = self.get_distance()
        cli.set('ultrasonic_M', M)
        time.sleep(0.2)
        
        pwm_S.setServoPwm('0',SERVO_ORIZON+30)
        R = self.get_distance()
        cli.set('ultrasonic_R', R)
        time.sleep(0.2)
        """
              
# Main program logic follows:
if __name__ == '__main__':
    print ('Ultrasonic is starting ... ')
    try:
        run()
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
        print("Ultrasonic is stopped")

