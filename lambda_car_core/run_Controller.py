import logging
import time
import RPi.GPIO as GPIO
from servo import *
from Motor import *
from PCA9685 import PCA9685
from redis import Redis
import cv2
import json

logging.basicConfig(level=logging.DEBUG, filename= './logs/raspberry_car.log', filemode = 'a',format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

cli = Redis('localhost')
CONTROL_CYCLE = 0.02 # Control cycle is every 20ms.
SERVO_ORIZON = 95
SERVO_VERTIC = 95
DEFAULT_PATH = '/home/pi/'


# Controller
# Request the sensor data from Redis every 20ms and control the motors, servos, camera to react: 
#          - Realtime Sensor data 
#          - AWS Cloud events

class Controller:
    def __init__(self):
        # Callibrate the Servo
        self.pwm_S=Servo()
        self.pwm_S.setServoPwm('0',SERVO_ORIZON)
        self.pwm_S.setServoPwm('1',SERVO_VERTIC)

        self.PWM = Motor()
        
    def navigate(self, infrared_LMR):
        logger.debug("Func_navigate: infrared_LMR =%d"%infrared_LMR)
        if infrared_LMR==2:
            logger.debug("Func_navigate: LMR=2")
            self.PWM.setMotorModel(800,800,800,800) #Forward
        if infrared_LMR==0:
            logger.debug("Func_navigate: LMR=0")
            self.PWM.setMotorModel(500,500,500,500) #Slow Forward
        elif infrared_LMR==4:
            logger.debug("Func_navigate: LMR=4")
            self.PWM.setMotorModel(-1500,-1500,2500,2500) #Left
        elif infrared_LMR==6:
            logger.debug("Func_navigate: LMR=6")
            self.PWM.setMotorModel(-2000,-2000,4000,4000) #Left ++
        elif infrared_LMR==1:
            logger.debug("Func_navigate: LMR=1")
            self.PWM.setMotorModel(2500,2500,-1500,-1500) #Right
        elif infrared_LMR==3:
            logger.debug("Func_navigate: LMR=3")
            self.PWM.setMotorModel(4000,4000,-2000,-2000) #Right ++
        elif infrared_LMR==7:
            logger.debug("Func_navigate: LMR=7")
            pass

    
    def save_image(self,img_pos):
        video_capture = cv2.VideoCapture(0)
        # Check success
        if not video_capture.isOpened():
            logger.debug("Func_Save_img: Could not open video device")
            raise Exception("Could not open video device")
            # Read picture. ret === True on success
        ret, frame = video_capture.read()
        video_capture.release()
        if ret and frame is not None:
            detection_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            img_local_path = DEFAULT_PATH+"camera_images/img_%s_%s.jpg"%(img_pos, detection_time)
            logger.debug("Func_Save_img: img_local_path: %s"%img_local_path)
            cv2.imwrite(img_local_path, frame)
        
            rfid_pos = "xe01" # to replace
            img_meta = {'img_local_path':img_local_path,'detection_time': detection_time, 'position':img_pos, 'rfid_pos':rfid_pos}
            img_meta = json.dumps(img_meta)
            logger.debug("Func_Save_img: --> image meta")
            logger.debug(img_meta)
            cli.rpush("car_images", img_meta)

    
    def obstacle_recognition(self):
        # Functions:
        # - Stop motor
        # - Measure the Left distance and Right distance to know the Object position.
        # - Take a picture of the obstacle and save it at local. -> save_image()
        
        obstacle_pos = "middle"

        self.PWM.setMotorModel(0,0,0,0)

        self.pwm_S.setServoPwm('0',SERVO_ORIZON-15)
        time.sleep(0.3)
        dist_L = int(cli.get('ultrasonic_M'))

        self.pwm_S.setServoPwm('0',SERVO_ORIZON)
        time.sleep(0.3)

        self.pwm_S.setServoPwm('0',SERVO_ORIZON+15)
        time.sleep(0.3)
        dist_R = int(cli.get('ultrasonic_M'))
        
        if dist_R < dist_L:
            logger.info("Func_Obstacle: Object on right")
            self.pwm_S.setServoPwm('0',SERVO_ORIZON+15)
            obstacle_pos = "right"
        else:
            logger.info("Func_Obstacle: Object on left")
            self.pwm_S.setServoPwm('0',SERVO_ORIZON-15)
            obstacle_pos = "left"

        self.save_image(obstacle_pos)

    def run(self):
        last_obstacle = 0
        
        while True:
            time.sleep(CONTROL_CYCLE)
            ultrasonic_M = int(cli.get('ultrasonic_M'))
            infrared_LMR = int(cli.get('infrared_LMR'))
            logger.debug("Func_Run: ultrasonic_M = %d; infrared_LMR = %d"%(ultrasonic_M,infrared_LMR))

            # Basic control modules: Obstacle recognition and Line Tracking. 
            if ultrasonic_M<30 and ((time.time()-last_obstacle)>5):
                logger.info("Func_Run: detect new obstacle")
                last_obstacle = time.time()
                self.obstacle_recognition()
            
            # elif cloud events

            else:
                logger.info("Func_Run: navigate...")
                self.navigate(infrared_LMR)


           

            
# Main program logic follows:
controller = Controller()
if __name__ == '__main__':
    print ('Controller is starting ... ')
    try:
        controller.run()
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
        controller.pwm_S.setServoPwm('0',SERVO_ORIZON)
        controller.PWM.setMotorModel(0,0,0,0)