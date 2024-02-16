import RPi.GPIO as GPIO
import time
import config
import threading

class ServoMotor(threading.Thread):
    """Threaded Servo Motor Class"""

    def __init__(self, amount_ingredient):
        threading.Thread.__init__(self) 
        self.event = threading.Event()  
        servoPIN = 23 # GPIO 23
        self.amount_ingredient = amount_ingredient
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(servoPIN, GPIO.OUT)

        self.p = GPIO.PWM(servoPIN, 50) # GPIO 23 as PWM with 50Hz
        self.p.start(2.5) # Initialisation

    def run(self):
        """Overwrite Thread.run(), called when the thread is started"""
        while self.event.is_set() == False:
            self.amount_controlling()
            time.sleep(0.5)

    def amount_controlling(self):

        if self.amount_ingredient == 1.5:
            self.move15ml()
        elif self.amount_ingredient == 2.5:
            self.move25ml()
        elif self.amount_ingredient == 5:
            self.move50ml()
        elif self.amount_ingredient == 7.5:
            self.move75ml()
        elif self.amount_ingredient == 10.0:
            self.move100ml()

        self.event.set()

    def move15ml(self):
            
        try:
            self.p.ChangeDutyCycle(2.5)  # Rotate to 0 degrees
            time.sleep(0.5)
            self.p.ChangeDutyCycle(7.5)  # Rotate to 90 degrees
            time.sleep(2)
            self.p.ChangeDutyCycle(2.5)  # Rotate back to 0 degrees
            time.sleep(0.5)

            print("ServoMotor: 15ml")
            self.p.stop()
            

        except KeyboardInterrupt:
            self.p.stop()
            print("ServoMotor: failure")

    def move25ml(self):

        try:
            self.p.ChangeDutyCycle(2.5)  # Rotate to 0 degrees
            time.sleep(0.5)
            self.p.ChangeDutyCycle(7.5)  # Rotate to 90 degrees
            time.sleep(3)
            self.p.ChangeDutyCycle(2.5)  # Rotate back to 0 degrees
            time.sleep(0.5)

            print("ServoMotor: 25ml")
            self.p.stop()

        except KeyboardInterrupt:
            self.p.stop()
            print("ServoMotor: failure")


    def move50ml(self):
            
        try:
            self.p.ChangeDutyCycle(2.5)  # Rotate to 0 degrees
            time.sleep(0.5)
            self.p.ChangeDutyCycle(7.5)  # Rotate to 90 degrees
            time.sleep(3)
            self.p.ChangeDutyCycle(2.5)  # Rotate back to 0 degrees
            time.sleep(3)
            self.p.ChangeDutyCycle(7.5)  # Rotate to 90 degrees
            time.sleep(3)
            self.p.ChangeDutyCycle(2.5)  # Rotate to 0 degrees
            time.sleep(0.5)

            print("ServoMotor: 50ml")
            self.p.stop()

        except KeyboardInterrupt:
            self.p.stop()
            print("ServoMotor: failure")

    def move75ml(self):

        try:
            self.p.ChangeDutyCycle(2.5)  # Rotate to 0 degrees
            time.sleep(0.5)
            self.p.ChangeDutyCycle(7.5)  # Rotate to 90 degrees
            time.sleep(3)
            self.p.ChangeDutyCycle(2.5)  # Rotate back to 0 degrees
            time.sleep(3)
            self.p.ChangeDutyCycle(7.5)  # Rotate to 90 degrees
            time.sleep(3)
            self.p.ChangeDutyCycle(2.5)  # Rotate to 0 degrees
            time.sleep(3)
            self.p.ChangeDutyCycle(7.5)  # Rotate to 90 degrees
            time.sleep(3)
            self.p.ChangeDutyCycle(2.5)  # Rotate to 0 degrees
            time.sleep(0.5)

            print("ServoMotor: 75ml")
            self.p.stop()

        except KeyboardInterrupt:
            self.p.stop()
            print("ServoMotor: failure")

    def move100ml(self):

        try:
            self.p.ChangeDutyCycle(2.5)  # Rotate to 0 degrees
            time.sleep(0.5)
            self.p.ChangeDutyCycle(7.5)  # Rotate to 90 degrees
            time.sleep(3)
            self.p.ChangeDutyCycle(2.5)  # Rotate back to 0 degrees
            time.sleep(3)
            self.p.ChangeDutyCycle(7.5)  # Rotate to 90 degrees
            time.sleep(3)
            self.p.ChangeDutyCycle(2.5)  # Rotate to 0 degrees
            time.sleep(3)
            self.p.ChangeDutyCycle(7.5)  # Rotate to 90 degrees
            time.sleep(3)
            self.p.ChangeDutyCycle(2.5)  # Rotate to 0 degrees
            time.sleep(3)
            self.p.ChangeDutyCycle(7.5)  # Rotate to 90 degrees
            time.sleep(3)
            self.p.ChangeDutyCycle(2.5)  # Rotate to 0 degrees
            time.sleep(0.5)

            print("ServoMotor: 100ml")
            self.p.stop()

        except KeyboardInterrupt:
            self.p.stop()
            print("ServoMotor: failure")