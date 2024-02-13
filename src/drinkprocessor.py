import logging
import config
import time
from StepperMotor.StepperMotor import StepperMotor
from ServoMotor.ServoMotor import ServoMotor
from RelayBoard.RelayBoard import RelayBoard
from WeightSensor.weightsensor import WeightSensor

class OrderQueue():

    def __init__(self):
        self.order_queue = []

    def setOrderQueue(self, order_queue):
        self.order_queue = order_queue

    def getOrderQueue(self):
        return self.order_queue
    
    def addOrder(self, recipe):
        # pass in a recipe object
        order = Order("TEST", recipe) 
        self.order_queue.append(order)

    def removeOrder(self, order):
        self.order_queue.remove(order)

    def clearOrderQueue(self):
        self.order_queue = []

    def printOrderQueue(self):
        for order in self.order_queue:
            print("Order: {0}".format(order.get('name')))

    def processOrderQueue(self):
        i = 1
        for order in self.order_queue:
            print("Process order: {0} of {1}".format(i, len(self.order_queue)))
            self.processOrder(order)
            i = i + 1

    def processOrder(self, order):
        print("Preparing Recipe: {0}".format(order.getRecipe().name))

        # process the order here ...
        print("*"*20)
        for ingredientDetail in order.getRecipe().ingredients_details:
                
            print("Zutat: {0}, Menge: {1}, Unit: {2}, Type: {3}, Position: {4}".format(ingredientDetail.getName(), \
                                                                                        ingredientDetail.getAmount(), \
                                                                                        ingredientDetail.getUnit(), \
                                                                                        ingredientDetail.getType(), \
                                                                                        ingredientDetail.getPosition()))
            
            
            
            
            self.CallStepperMotor(ingredientDetail.getPosition())
            time.sleep(1)
            if ingredientDetail.getType() == "gravity":
                self.CallServoMotor(ingredientDetail.getAmount())
            else:
                self.CallRelayBoard(ingredientDetail.getAmount(), ingredientDetail.getName())
            time.sleep(1)
            self.CallWeightSensor(ingredientDetail.getAmount())

        self.stepm.back_to_startposition()

        print("*"*20)
        
            #main.CallWeightSensor()
                
    def CallStepperMotor(self, position_ingredient):
        logging.info("Calling StepperMotor")
        self.stepm = StepperMotor(position_ingredient)
        self.stepm.start()
        self.stepm.join()
        logging.info("Calling StepperMotor: {0}".format(self.stepm))

    def CallServoMotor(self, amount_ingredient):
        logging.info("Calling ServoMotor")
        self.servm = ServoMotor(amount_ingredient)
        self.servm.start()
        self.servm.join()
        logging.info("Calling ServoMotor: {0}".format(self.servm))

    def CallRelayBoard(self, amount_ingredient, ingredient_name):
        logging.info("Calling RelayBoard")
        self.relayb = RelayBoard(amount_ingredient, ingredient_name)
        self.relayb.start()
        self.relayb.join()
        logging.info("Calling RelayBoard: {0}".format(self.relayb))
    
    def CallWeightSensor(self, amount_ingredient):
        logging.info("Calling WeightSensor")
        self.weights = WeightSensor(amount_ingredient)
        self.weights.start()
        self.weights.join()
        logging.info("Calling WeightSensor: {0}".format(self.weights))

class Order():
    
        def __init__(self, name=None, recipe=None):
            self.name = name
            self.recipe = recipe
            self.customer = None

        def setName(self, name):
            self.name = name
    
        def getName(self):
            return self.name
        
        def setCustomer(self, customer):
            self.customer = customer   

        def getCustomer(self):
            return self.customer
        
        def setRecipe(self, recipe):
            self.recipe = recipe

        def getRecipe(self):
            return self.recipe

        

class Customer():

    def __init__(self, name=None):
        self.name = name

    def setName(self, name):
        self.name = name

    def getName(self):
        return self.name




class Recipe():
    # This class is used to store the details of a recipe
    def __init__(self, search_string=None):
        
        self.search_string = search_string
        self.recipe = None
        self.name = None
        self.ingredients = []
        self.ingredients_details = []

        self.findRecipes()


    def findRecipes(self):
        # search for a recipe
        logging.info("Reading recipes")
        
        for recipe in config.recipes:

            if recipe.get('name') == self.search_string:

                msg = "Rezept: {0}, Anzahl: {1}".format(recipe.get('name'), len(config.recipes))
                logging.info(msg)
                self.recipe = recipe
                self.name = recipe.get('name')
                self.ingredients = recipe.get('ingredients')

                for ingredient in recipe.get('ingredients'):
                    msg = "Ingredient: {0}, Menge: {1}, Unit: {2}".format(ingredient.get('ingredient'), ingredient.get('amount'), ingredient.get('unit'))
                    logging.info(msg)

                    ingredientDetails = IngredientDetails()
                    ingredientDetails.setName(ingredient.get('ingredient'))
                    ingredientDetails.setAmount(ingredient.get('amount'))
                    ingredientDetails.setUnit(ingredient.get('unit'))
                    ingredientDetails.setPosition(self.getBottle(ingredient.get('ingredient')).get('position'))            
                    ingredientDetails.setType(self.getBottle(ingredient.get('ingredient')).get('type'))

                    self.ingredients_details.append(ingredientDetails)



    def getBottle(self, ingredient):
        # Details der Flasche aus der Konfiguration holen, inkl. Position und Typ
        for bottle in config.bottle_inventory:
            if bottle.get('name') == ingredient:
                msg = "Bottle: {0}, Position: {1}, Type: {2}".format(bottle.get('name'), bottle.get('position'), bottle.get('type'))
                #print('In getBottle: {0}'.format(msg))
                #logging.info(msg)
                return bottle


        
            


class IngredientDetails():
    # This class is used to store the details of an ingredient
    def __init__(self, name=None, amount=None, unit=None):
        self.name = name
        self.amount = amount
        self.unit = unit
        self.position = None
        self.type = None

    def setName(self, name):
        self.name = name
    
    def getName(self):
        return self.name
        
    def setAmount(self, amount):
        self.amount = amount   

    def getAmount(self):
        return self.amount
        
    def setUnit(self, unit):
        self.unit = unit

    def getUnit(self):
        return self.unit
    
    def setPosition(self, position):
        self.position = position

    def getPosition(self):
        return self.position
    
    def setType(self, type):
        self.type = type

    def getType(self):  
        return self.type

    

        
            



            
