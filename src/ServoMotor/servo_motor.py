import RPi.GPIO as GPIO
import time

class ServoMotor:
    def __init__(self, pin):
        self.pin = pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)
        self.pwm = GPIO.PWM(self.pin, 50)  # 50 Hz frequency for servo motor

    def set_angle(self, angle):
        duty_cycle = angle / 18 + 2  # Convert angle to duty cycle
        self.pwm.start(duty_cycle)
        time.sleep(1)  # Wait for the servo to reach the desired position
        self.pwm.stop()

    def cleanup(self):
        GPIO.cleanup()
