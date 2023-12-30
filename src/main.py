import logging
import os
import json
import config
import drinkprocessor


import StepperMotor.StepperMotor as SM

# Create the logs folder if it doesn't exist
logs_folder = 'logs'
os.makedirs(logs_folder, exist_ok=True)

# Configure the logger
logging.basicConfig(filename=os.path.join(logs_folder, 'logfile.log'), level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')



class Main:
    def __init__(self):
        pass
    

    def CallDrinkProcessor(self):
        logging.info("Calling DrinkProcessor")
        
        # search for a recipe. in this example, we search for a Mojito
        search_string = "Mojito"
        recipe = drinkprocessor.Recipe(search_string=search_string)
        
        # add an order to the order queue
        orderqueue = drinkprocessor.OrderQueue()
        orderqueue.addOrder(recipe)

        print("Order Queue Länge: {0}".format(len(orderqueue.getOrderQueue()))) 

        # print the order queue
        for order in orderqueue.getOrderQueue():
            print("Order: {0}".format(order.getRecipe()))
        

        # process the order queue
        #orderqueue.processOrderQueue()
        


    def CallStepperMotor(self):
        logging.info("Calling StepperMotor")
        sm = SM.StepperMotor()
        sm.nema17_ramp(3200, 400)


        


if __name__ == "__main__":
    # Create an instance of the Main class
    main = Main()

    # Call the CallDrinkProcessor method
    main.CallDrinkProcessor()

    # Call the CallStepperMotor method
    #main.CallStepperMotor()

    