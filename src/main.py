import logging
import os
import json
import config


import StepperMotor.StepperMotor as SM

# Create the logs folder if it doesn't exist
logs_folder = 'logs'
os.makedirs(logs_folder, exist_ok=True)

# Configure the logger
logging.basicConfig(filename=os.path.join(logs_folder, 'logfile.log'), level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')



class Main:
    def __init__(self):
        pass
    

    def CallStepperMotor(self):
        logging.info("Calling StepperMotor")
        sm = SM.StepperMotor()
        sm.nema17_ramp(3200, 400)
        


if __name__ == "__main__":
    # Create an instance of the Main class
    main = Main()

    # Call the CallStepperMotor method
    main.CallStepperMotor()

    