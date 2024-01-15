import logging
import config




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

    def __init__(self, search_string=None):
        
        self.search_string = search_string
        self.recipe = None
        self.name = None
        self.ingredients = []

        self.findRecipes()


    def findRecipes(self):
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

        
            



            
