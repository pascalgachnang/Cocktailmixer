import logging
import RPi.GPIO as GPIO
import time
import os
from   StepperMotor.DRV8825 import DRV8825
import config
import threading


logs_folder = 'logs'

class StepperMotor(threading.Thread):
    """Threaded Stepper Motor Class"""

    def __init__(self, total_steps, acceleration_steps):
        threading.Thread.__init__(self) 
        self.event = threading.Event()       
        self.config = config.config
        self.stepdelay_start = self.config.getfloat('MotorSteuerung', 'stepdelay_start')
        self.stepdelay_end = self.config.getfloat('MotorSteuerung', 'stepdelay_end')
        
        self.Motor1 = DRV8825(dir_pin=13, step_pin=19, enable_pin=12, mode_pins=(16, 17, 20))
        # self.Motor2 = DRV8825(dir_pin=24, step_pin=18, enable_pin=4, mode_pins=(21, 22, 27))
 
        self.total_steps = total_steps
        self.acceleration_steps = acceleration_steps

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


    def run(self):
        """Overwrite Thread.run(), called when the thread is started"""
        while self.event.is_set() == False:
            self._nema17_ramp()
            time.sleep(0.5)

    def _nema17_ramp(self):
       
        # accelerationramp
        for i in range(self.acceleration_steps):
            current_stepdelay = self.stepdelay_start + (self.stepdelay_end - self.stepdelay_start) * i / self.acceleration_steps
            self.perform_step(current_stepdelay)

        # fullspeed-phase
        for i in range(self.acceleration_steps, self.total_steps - self.acceleration_steps):
            self.perform_step(self.stepdelay_end)

        # decelerationramp
        for i in range(self.total_steps - self.acceleration_steps, self.total_steps):
            current_stepdelay = self.stepdelay_start + (self.stepdelay_end - self.stepdelay_start) * (self.total_steps - i) / self.acceleration_steps
            self.perform_step(current_stepdelay)

        self.Motor1.Stop()
        self.event.set()
        #GPIO.cleanup()