import logging
import RPi.GPIO as GPIO
import time
import os
from   StepperMotor.DRV8825 import DRV8825
import config
import threading


logs_folder = 'logs'
end_switch_pin = 22
       


class StepperMotor(threading.Thread):
    """Threaded Stepper Motor Class"""

    def __init__(self, total_steps, acceleration_steps):
        threading.Thread.__init__(self) 
        self.event = threading.Event()       
        self.config = config.config
        self.stepdelay_start = self.config.getfloat('MotorSteuerung', 'stepdelay_start')
        self.stepdelay_end = self.config.getfloat('MotorSteuerung', 'stepdelay_end')
        self.stepdelay_end_reference_run = self.config.getfloat('MotorSteuerung', 'stepdelay_end_reference_run')
        self.end_switch_pin = end_switch_pin
        
        self.Motor1 = DRV8825(dir_pin=13, step_pin=19, enable_pin=12, mode_pins=(16, 17, 20))
        # self.Motor2 = DRV8825(dir_pin=24, step_pin=18, enable_pin=4, mode_pins=(21, 22, 27))
 
        self.total_steps = total_steps
        self.acceleration_steps = acceleration_steps

        # Set the end switch pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.end_switch_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        


    def perform_step(self, stepdelay):
        # Perform the step with the given step delay
        self.Motor1.TurnStep(Dir='forward', steps=1, stepdelay=stepdelay)


    def write_values_to_file(self, values):
        # Open the file in append mode
        with open(os.path.join(logs_folder, 'values.csv'), "w") as file:
            
            for value in values:
                # Write the list of values to the file
                file.write("\n".join(values) + "\n")

    def motor_direction(self):
        # Set the direction of the stepper motor
        self.motor_direction 


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

        
    def reference_run(self):
        try:

            # accelerationramp
            for i in range(self.acceleration_steps):
                current_stepdelay_reference_run = self.stepdelay_start + (self.stepdelay_end_reference_run - self.stepdelay_start) * i / self.acceleration_steps
                self.perform_step(current_stepdelay_reference_run)

                if self.is_end_switch_triggered(): # end switch triggered
                    print("end switch triggered")
                    self.Motor1.Stop()
                    self.current_position = 0
                    print("positioning steppermotor completed")
                    return

            # fullspeed-phase
            while not self.is_end_switch_triggered():
                self.perform_step(self.stepdelay_end_reference_run)

                if self.is_end_switch_triggered(): # end switch triggered
                    print("end switch triggered")
                    self.current_position = 0
                    print("positioning steppermotor completed")
                    self.Motor1.Stop()
                    return

        finally:
            self.Motor1.Stop()
            GPIO.cleanup()

    def position_stepper(self):

        self.next_position = self.position
        self.alkohol = alkohol_zuweisungen.get(position, "Keine Zuweisung gefunden")    
            

    def is_end_switch_triggered(self):
        # Check if the end switch is triggered
        return GPIO.input(self.end_switch_pin) == GPIO.LOW
    
            
    

        



        