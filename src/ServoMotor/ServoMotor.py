from rpi_hardware_pwm import HardwarePWM
import time

class ServoMotor():

    PWM_CHANNEL = 0
    PWM_FREQ = 50
    CHIP = 0

    POSITION_SPENDER = 2.8
    POSITION_HOME = 8

    def __init__(self):
        self.p = HardwarePWM(pwm_channel = self.PWM_CHANNEL, hz = self.PWM_FREQ, chip = self.CHIP)
        self.p.start(self.POSITION_HOME)
        

    def cleanupServo(self):
        self.p.stop()
        #GPIO.cleanup()


    def amount_controlling(self, amount_ingredient):
        fncMap = {
            1:   self.move50ml,
            1.5: self.move50ml,
            2.5: self.move50ml,
            5:   self.move50ml,
            6:   self.move50ml,
            7.5: self.move50ml,
            10.0: self.move50ml 
        }

        try:
            fnc = fncMap[amount_ingredient]
            fnc()
        except KeyError:
            print("error")


    def setPosition(self, position):
        self.p.change_duty_cycle(position)

    def move15ml(self):
            
        try:
            # Rotate to 45 degrees
            self.p.change_duty_cycle(2.5)  # Rotate to 0 degrees
            time.sleep(0.5)
            self.p.change_duty_cycle(7.5)  # Rotate to 90 degrees
            time.sleep(2)
            self.p.change_duty_cycle(2.5)  # Rotate back to 0 degrees
            time.sleep(0.5)

            print("ServoMotor: 15ml")
            self.p.stop()
            

        except KeyboardInterrupt:
            self.p.stop()
            print("ServoMotor: failure")

    def move25ml(self):

        try:
            self.p.change_duty_cycle(5)  # Rotate to 0 degrees
            time.sleep(0.5)
            self.p.change_duty_cycle(2.5)  # Rotate to 90 degrees
            time.sleep(3)
            self.p.change_duty_cycle(5)  # Rotate back to 0 degrees
            time.sleep(0.5)

            print("ServoMotor: 25ml")
            self.p.stop()

        except KeyboardInterrupt:
            self.p.stop()
            print("ServoMotor: failure")


    def move50ml(self):
            
        try:
            self.p.change_duty_cycle(self.POSITION_SPENDER)  # Rotate to 0 degrees
            time.sleep(3)
            self.p.change_duty_cycle(self.POSITION_HOME)  # Rotate back to 45 degrees
            time.sleep(3)
            self.p.change_duty_cycle(self.POSITION_SPENDER)  # Rotate to 0 degrees
            time.sleep(3)
            self.p.change_duty_cycle(self.POSITION_HOME)  # Rotate to 45 degrees

            print("ServoMotor: 50ml")
            #self.p.stop()

        except KeyboardInterrupt:
            self.p.stop()
            print("ServoMotor: failure")

    def move60ml(self):
            
        try:
            self.p.change_duty_cycle(2.5)  # Rotate to 0 degrees
            time.sleep(0.5)
            self.p.change_duty_cycle(7.5)  # Rotate to 90 degrees
            time.sleep(3)
            self.p.change_duty_cycle(2.5)  # Rotate back to 0 degrees
            time.sleep(3)
            self.p.change_duty_cycle(7.5)  # Rotate to 90 degrees
            time.sleep(3)
            self.p.change_duty_cycle(2.5)  # Rotate to 0 degrees
            time.sleep(0.5)
            self.p.change_duty_cycle(7.5)  # Rotate to 90 degrees
            time.sleep(1.5)
            self.p.change_duty_cycle(2.5)  # Rotate to 0 degrees
            time.sleep(0.5)
            
            print("ServoMotor: 60ml")
            self.p.stop()

        except KeyboardInterrupt:
            self.p.stop()
            print("ServoMotor: failure")

    def move75ml(self):

        try:
            self.p.change_duty_cycle(2.5)  # Rotate to 0 degrees
            time.sleep(0.5)
            self.p.change_duty_cycle(7.5)  # Rotate to 90 degrees
            time.sleep(3)
            self.p.change_duty_cycle(2.5)  # Rotate back to 0 degrees
            time.sleep(3)
            self.p.change_duty_cycle(7.5)  # Rotate to 90 degrees
            time.sleep(3)
            self.p.change_duty_cycle(2.5)  # Rotate to 0 degrees
            time.sleep(3)
            self.p.change_duty_cycle(7.5)  # Rotate to 90 degrees
            time.sleep(3)
            self.p.change_duty_cycle(2.5)  # Rotate to 0 degrees
            time.sleep(0.5)

            print("ServoMotor: 75ml")
            self.p.stop()

        except KeyboardInterrupt:
            self.p.stop()
            print("ServoMotor: failure")

    def move100ml(self):

        try:
            self.p.change_duty_cycle(2.5)  # Rotate to 0 degrees
            time.sleep(0.5)
            self.p.change_duty_cycle(7.5)  # Rotate to 90 degrees
            time.sleep(3)
            self.p.change_duty_cycle(2.5)  # Rotate back to 0 degrees
            time.sleep(3)
            self.p.change_duty_cycle(7.5)  # Rotate to 90 degrees
            time.sleep(3)
            self.p.change_duty_cycle(2.5)  # Rotate to 0 degrees
            time.sleep(3)
            self.p.change_duty_cycle(7.5)  # Rotate to 90 degrees
            time.sleep(3)
            self.p.change_duty_cycle(2.5)  # Rotate to 0 degrees
            time.sleep(3)
            self.p.change_duty_cycle(7.5)  # Rotate to 90 degrees
            time.sleep(3)
            self.p.change_duty_cycle(2.5)  # Rotate to 0 degrees
            time.sleep(0.5)

            print("ServoMotor: 100ml")
            self.p.stop()

        except KeyboardInterrupt:
            self.p.stop()
            print("ServoMotor: failure")