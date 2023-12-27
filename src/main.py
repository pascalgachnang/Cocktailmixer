import logging
import os
import json
import configparser

import StepperMotor.StepperMotor as SM

# Create the logs folder if it doesn't exist
logs_folder = 'logs'
os.makedirs(logs_folder, exist_ok=True)

# Configure the logger
logging.basicConfig(filename=os.path.join(logs_folder, 'logfile.log'), level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


# Load the config file
config_folder = 'config'
config_file = os.path.join(config_folder, 'config.ini')
config = configparser.ConfigParser()
config.read(config_file)


class Main:
    def __init__(self):
        
        # Access config values
        self.stepdelay = config.getfloat('MotorSteuerung', 'stepdelay')

    def CallStepperMotor(self):
        logging.info("Calling StepperMotor")
        sm = SM.StepperMotor()
        sm.run(self.stepdelay)
        


if __name__ == "__main__":
    # Create an instance of the Main class
    main = Main()

    # Call the CallStepperMotor method
    main.CallStepperMotor()