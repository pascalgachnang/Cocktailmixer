import logging
import RPi.GPIO as GPIO
import time
import os
from   StepperMotor.DRV8825 import DRV8825

#logger = logging.getLogger(__name__)

logs_folder = 'logs'

class StepperMotor:
    def __init__(self):
        self.Motor1 = DRV8825(dir_pin=13, step_pin=19, enable_pin=12, mode_pins=(16, 17, 20))
        # self.Motor2 = DRV8825(dir_pin=24, step_pin=18, enable_pin=4, mode_pins=(21, 22, 27))

        self.stepdelay = 0.0001

    def run(self, stepdelay):

        self.stepdelay = stepdelay

        #logging.info("In Class StepperMotor")
        #logging.info("Stepdelay is: {0}".format(self.stepdelay))
        print("Stepdelay is: {0}".format(self.stepdelay))

        try:
            self.Motor1.SetMicroStep('software','1/8step')

            # Acceleration ramp
            acceleration_time = 1  # seconds
            acceleration_steps = 800  # half of the total steps
            acceleration_delay = acceleration_time / acceleration_steps

            for i in range(acceleration_steps):
                self.Motor1.TurnStep(Dir='forward', steps=1, stepdelay=self.stepdelay)
                time.sleep(acceleration_delay)

            # Constant speed
            self.Motor1.TurnStep(Dir='forward', steps=5000 - acceleration_steps, stepdelay=self.stepdelay)

            # Deceleration ramp
            deceleration_time = 1  # seconds
            deceleration_steps = 800  # half of the total steps
            deceleration_delay = deceleration_time / deceleration_steps

            for i in range(deceleration_steps):
                self.Motor1.TurnStep(Dir='forward', steps=1, stepdelay=self.stepdelay)
                time.sleep(deceleration_delay)
            

        except:
            print("\nMotor stop")
            self.Motor1.Stop()
            GPIO.cleanup()


    def accelerate_motor(self, start_stepdelay, end_stepdelay, total_steps, total_time):
            
            current_stepdelay = start_stepdelay
            acceleration_delay = (end_stepdelay - start_stepdelay) / total_steps

            for i in range(total_steps):
                self.Motor1(steps=1, stepdelay=current_stepdelay)
                current_stepdelay += acceleration_delay
                time.sleep(total_time / total_steps)
             
    
    

    def nema17_ramp(self, start_stepdelay, end_stepdelay, total_steps, total_time):
        current_stepdelay = start_stepdelay
        acceleration_delay = (end_stepdelay - start_stepdelay) / total_steps
        value_list = []

        for i in range(total_steps):
            # Perform acceleration ramp
            if i < total_steps / 2:
                current_stepdelay += acceleration_delay
            # Perform deceleration ramp
            else:
                current_stepdelay -= acceleration_delay

            # Perform step with the current step delay
            logging.info("Stepdelay is: {0}".format(current_stepdelay))
            
            # Append each value to a list for visualization
            value_list.append(str(current_stepdelay))

            self.perform_step(current_stepdelay)

            # Wait for the specified time per step
            time.sleep(total_time / total_steps)



        # Write the list of values to a file
        #self.write_values_to_file(value_list)

        logging.info("\nMotor stop")
        self.Motor1.Stop()
        GPIO.cleanup()


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



    start_stepdelay = 0.1
    end_stepdelay = 0.001
    total_steps = 1600  # 1600 Schritte pro Umdrehung
    total_time = 2  # Gesamtdauer in Sekunden