from rpi_hardware_pwm import HardwarePWM
import time

class ServoMotor():


    # RaspberryPI 3,4
    #PWM_CHANNEL = 0
    #PWM_FREQ = 50
    #CHIP = 0


    # RaspberryPI 5
    # For Rpi 1,2,3,4, use chip=0; For Rpi 5, use chip=2 
    PWM_CHANNEL = 2
    PWM_FREQ = 50
    CHIP = 2


    POSITION_SPENDER = 2.65
    POSITION_HOME = 4.5

    def __init__(self):
        self.p = HardwarePWM(pwm_channel = self.PWM_CHANNEL, hz = self.PWM_FREQ, chip = self.CHIP)
        self.p.start(self.POSITION_HOME)
        

    def cleanupServo(self):
        self.p.stop()
        #GPIO.cleanup()


    def amount_controlling(self, amount_ingredient):
        fncMap = {
            1.5: self.move15ml,
            2.5: self.move25ml,
            4:   self.move40ml,
            5:   self.move50ml,
            6:   self.move60ml,
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
            self.p.change_duty_cycle(self.POSITION_SPENDER)  # Rotate to 0 degrees
            time.sleep(2)
            self.p.change_duty_cycle(self.POSITION_HOME)  # Rotate back to 45 degrees

            print("ServoMotor: 50ml")
            #self.p.stop()

        except KeyboardInterrupt:
            self.p.stop()
            print("ServoMotor: failure")

    def move25ml(self):

        try:
            self.p.change_duty_cycle(self.POSITION_SPENDER)  # Rotate to 0 degrees
            time.sleep(3.5)
            self.p.change_duty_cycle(self.POSITION_HOME)  # Rotate back to 45 degrees

            print("ServoMotor: 50ml")
            #self.p.stop()

        except KeyboardInterrupt:
            self.p.stop()
            print("ServoMotor: failure")


    def move40ml(self):
            
        try:
            self.p.change_duty_cycle(self.POSITION_SPENDER)  # Rotate to 0 degrees
            time.sleep(3.5)
            self.p.change_duty_cycle(self.POSITION_HOME)  # Rotate back to 45 degrees
            time.sleep(3)
            self.p.change_duty_cycle(self.POSITION_SPENDER)  # Rotate to 0 degrees
            time.sleep(2.5)
            self.p.change_duty_cycle(self.POSITION_HOME)  # Rotate to 45 degrees

            print("ServoMotor: 50ml")
            #self.p.stop()

        except KeyboardInterrupt:
            self.p.stop()
            print("ServoMotor: failure")


    def move50ml(self):
            
        try:
            self.p.change_duty_cycle(self.POSITION_SPENDER)  # Rotate to 0 degrees
            time.sleep(3.5)
            self.p.change_duty_cycle(self.POSITION_HOME)  # Rotate back to 45 degrees
            time.sleep(3)
            self.p.change_duty_cycle(self.POSITION_SPENDER)  # Rotate to 0 degrees
            time.sleep(3.5)
            self.p.change_duty_cycle(self.POSITION_HOME)  # Rotate to 45 degrees

            print("ServoMotor: 50ml")
            #self.p.stop()

        except KeyboardInterrupt:
            self.p.stop()
            print("ServoMotor: failure")

    def move60ml(self):
            
        try:
            self.p.change_duty_cycle(self.POSITION_SPENDER)  # Rotate to 0 degrees
            time.sleep(3.5)
            self.p.change_duty_cycle(self.POSITION_HOME)  # Rotate back to 45 degrees
            time.sleep(3)
            self.p.change_duty_cycle(self.POSITION_SPENDER)  # Rotate to 0 degrees
            time.sleep(3.5)
            self.p.change_duty_cycle(self.POSITION_HOME)  # Rotate to 45 degrees
            time.sleep(3)
            self.p.change_duty_cycle(self.POSITION_SPENDER)  # Rotate to 0 degrees
            time.sleep(1.5)
            self.p.change_duty_cycle(self.POSITION_HOME)  # Rotate to 45 degrees

            print("ServoMotor: 50ml")
            #self.p.stop()

        except KeyboardInterrupt:
            self.p.stop()
            print("ServoMotor: failure")


    