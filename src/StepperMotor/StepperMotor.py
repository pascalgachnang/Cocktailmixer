import logging
import RPi.GPIO as GPIO
import time
import os
from   StepperMotor.DRV8825 import DRV8825
import config
import threading


logs_folder = 'logs'
end_switch_pin = 22
       


class StepperMotor():
    def __init__(self, acceleration_steps = 800):    
        self.config = config.config
        self.stepdelay_start = self.config.getfloat('MotorSteuerung', 'stepdelay_start')
        self.stepdelay_end = self.config.getfloat('MotorSteuerung', 'stepdelay_end')
        self.stepdelay_end_reference_run = self.config.getfloat('MotorSteuerung', 'stepdelay_end_reference_run')
        self.end_switch_pin = end_switch_pin
        self.current_position = 0
        self.motor_direction = 'backward'
        
        self.total_steps = None
        self.acceleration_steps = acceleration_steps

        
        # Set the end switch pin
        GPIO.setmode(GPIO.BCM)
        self.Motor1 = DRV8825(dir_pin=13, step_pin=19, enable_pin=12, mode_pins=(16, 17, 20))
        # self.Motor2 = DRV8825(dir_pin=24, step_pin=18, enable_pin=4, mode_pins=(21, 22, 27))
        GPIO.setup(self.end_switch_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        

    def perform_step(self, stepdelay):
        # Perform the step with the given step delay
        self.Motor1.TurnStep(Dir=self.motor_direction, steps=1, stepdelay=stepdelay)


    def write_values_to_file(self, values):
        # Open the file in append mode
        with open(os.path.join(logs_folder, 'values.csv'), "w") as file:
            
            for value in values:
                # Write the list of values to the file
                file.write("\n".join(values) + "\n")



    def move(self, position_ingredient):
        self._momental_position(position_ingredient)
        self._nema17_ramp()


    def _nema17_ramp(self):
        # accelerationramp

        if abs(self.total_steps) - 2*self.acceleration_steps < 0:
            self.acceleration_steps = self.total_steps // 2

        for i in range(self.acceleration_steps):
            current_stepdelay = round(self.stepdelay_start + (self.stepdelay_end - self.stepdelay_start) * i / self.acceleration_steps, 7)
            self.perform_step(current_stepdelay)

        # fullspeed-phase
        for i in range(self.acceleration_steps, abs(self.total_steps) - self.acceleration_steps):
            self.perform_step(self.stepdelay_end)

        # decelerationramp
        for i in range(abs(self.total_steps) - self.acceleration_steps, abs(self.total_steps)):
            current_stepdelay = round(self.stepdelay_start + (self.stepdelay_end - self.stepdelay_start) * (abs(self.total_steps) - i) / self.acceleration_steps, 7)
            self.perform_step(current_stepdelay)

        self.Motor1.Stop()
        

        
    def reference_run(self):
        # Reference run of the stepper motor
        self.motor_direction = 'forward'

        try:

            # accelerationramp
            for i in range(self.acceleration_steps):
                current_stepdelay_reference_run = self.stepdelay_start + (self.stepdelay_end_reference_run - self.stepdelay_start) * i / self.acceleration_steps
                self.perform_step(current_stepdelay_reference_run)

                if self._is_end_switch_triggered(): # end switch triggered
                    print("end switch triggered")
                    self.Motor1.Stop()
                    self.current_position = 0
                    print("positioning steppermotor completed")
                    return

            # fullspeed-phase
            while not self._is_end_switch_triggered():
                self.perform_step(current_stepdelay_reference_run)

                if self._is_end_switch_triggered(): # end switch triggered
                    print("end switch triggered")
                    self.current_position = 0
                    print("positioning steppermotor completed")
                    self.Motor1.Stop()
                    return

        finally:
            self.Motor1.Stop()
    

    

    def _is_end_switch_triggered(self):
        # Check if the end switch is triggered
        return GPIO.input(self.end_switch_pin) == GPIO.LOW
    
            
    def _momental_position(self, position_ingredient):
        # Calculate the current position of the stepper motor
        
        self.total_steps = position_ingredient - self.current_position

        # Bestimme die Richtung des Schrittmotors
        self.motor_direction = 'backward' if self.total_steps > 0 else 'forward'
        print("current position: ", self.current_position, "motor direction: ", self.motor_direction)

        # Aktualisiere die aktuelle Position
        self.current_position = position_ingredient
        
        if self.total_steps >= 0:
            return self.total_steps
        else:
            return -self.total_steps

    def back_to_startposition(self):
        # Back to start position
        self.acceleration_steps = 800
        self.total_steps = 200 - self.current_position 
        
        if abs(self.total_steps) - 2*self.acceleration_steps < 0:
            self.acceleration_steps = self.total_steps // 2

        self.motor_direction = 'forward' 
        self._nema17_ramp()
        time.sleep(0.5)
        print("back to start position completed")
        self.current_position = 200
    



        