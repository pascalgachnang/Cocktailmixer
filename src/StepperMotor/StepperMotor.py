import logging
import RPi.GPIO as GPIO
import time
import os
from   StepperMotor.DRV8825 import DRV8825
import config

#logger = logging.getLogger(__name__)

logs_folder = 'logs'

class StepperMotor:
    def __init__(self):
        
        self.config = config.config
        self.stepdelay_start = self.config.getfloat('MotorSteuerung', 'stepdelay_start')
        self.stepdelay_end = self.config.getfloat('MotorSteuerung', 'stepdelay_end')
        
        self.Motor1 = DRV8825(dir_pin=13, step_pin=19, enable_pin=12, mode_pins=(16, 17, 20))
        # self.Motor2 = DRV8825(dir_pin=24, step_pin=18, enable_pin=4, mode_pins=(21, 22, 27))

     

    def perform_step(self, stepdelay):
        # Perform the step with the given step delay
        # Replace this with your actual code to control the stepper motor
        self.Motor1.TurnStep(Dir='forward', steps=1, stepdelay=stepdelay)


    def write_values_to_file(self, values):
        # Open the file in append mode
        with open(os.path.join(logs_folder, 'values.csv'), "w") as file:
            
            for value in values:
                # Write the list of values to the file
                file.write("\n".join(values) + "\n")



    def nema17_ramp(self, total_steps, acceleration_steps):
       
        # accelerationramp
        for i in range(acceleration_steps):
            current_stepdelay = self.stepdelay_start + (self.stepdelay_end - self.stepdelay_start) * i / acceleration_steps
            self.perform_step(current_stepdelay)

        # fullspeed-phase
        for i in range(acceleration_steps, total_steps - acceleration_steps):
            self.perform_step(self.stepdelay_end)

        # decelerationramp
        for i in range(total_steps - acceleration_steps, total_steps):
            current_stepdelay = self.stepdelay_start + (self.stepdelay_end - self.stepdelay_start) * (total_steps - i) / acceleration_steps
            self.perform_step(current_stepdelay)


        self.Motor1.Stop()
        GPIO.cleanup()