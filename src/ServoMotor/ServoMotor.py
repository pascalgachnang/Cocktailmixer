import RPi.GPIO as GPIO
import time
import config


class ServoMotor:

    def __init__(self):
        servoPIN = 23 # GPIO 23
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(servoPIN, GPIO.OUT)

        self.p = GPIO.PWM(servoPIN, 50) # GPIO 23 as PWM with 50Hz
        self.p.start(2.5) # Initialisation

    def move25ml(self):

        try:
            self.p.ChangeDutyCycle(2.5)  # Rotate to 0 degrees
            time.sleep(0.5)
            self.p.ChangeDutyCycle(7.5)  # Rotate to 90 degrees
            time.sleep(3)
            self.p.ChangeDutyCycle(2.5)  # Rotate back to 0 degrees
            time.sleep(0.5)

        except KeyboardInterrupt:
            self.p.stop()
            GPIO.cleanup()


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

        except KeyboardInterrupt:
            self.p.stop()
            GPIO.cleanup()