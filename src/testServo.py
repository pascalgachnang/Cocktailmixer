
import time


from ServoMotor.ServoMotor import ServoMotor


# servo = ServoMotor()

# servo.setPosition(5)
# time.sleep(3)
# servo.setPosition(7.5)
# servo.amount_controlling(5)
# print("ServoMotor: 5ml")
# time.sleep(2)

# servo.amount_controlling(1.5)
# print("ServoMotor: 1.5ml")

# servo.cleanupServo()


import RPi.GPIO as GPIO
from time import sleep

## add your servo BOARD PIN number ##
servo_pin = 23

GPIO.setmode(GPIO.BCM)
GPIO.setup(servo_pin, GPIO.OUT)

pwm=GPIO.PWM(servo_pin, 50)
pwm.start(0)

## edit these duty cycle % values ##
left = 2.5
neutral = 7.5
right = 12
#### that's all folks ####

print("begin test")

print("duty cycle", left,"% at left -90 deg")
pwm.ChangeDutyCycle(2.5)
sleep(1)

print("duty cycle", neutral,"% at 0 deg")
pwm.ChangeDutyCycle(neutral)
sleep(1)

print("duty cycle",right, "% at right +90 deg")
pwm.ChangeDutyCycle(right)
sleep(1)

print("end of test")

pwm.stop()
GPIO.cleanup()
