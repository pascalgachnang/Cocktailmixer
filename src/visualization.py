import kivy
import logging
import time
import drinkprocessor
from kivy.app import App
from kivy.uix.widget import Widget  
from kivy.uix.button import Button  
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from StepperMotor.StepperMotor import StepperMotor
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock

class MyLayout(Widget):
    pass

#Layouts for the windows
class PasswordWindow(Screen): #Layout for the password window
    pass

class PositioningWindow(Screen): #Layout for the positioning window
    pass

class MainWindow1(Screen): #Layout for the main window, first page
    pass

class MainWindow2(Screen): #Layout for the main window, second page
    pass

class DrinkInProgress(Screen): #Layout for the drink in progress window
    pass

    

        

class WindowManager(ScreenManager):
    pass

# Load the kv file
kv = Builder.load_file("my.kv")

class MyCocktailmixerApp(App):
    def build(self):
        self.drinkprocessor = drinkprocessor.OrderQueue()
        self.drinkprocessor.start()
        self.lastclicktime = None
        self.steppermotor = StepperMotor()
        return kv 

    
    def IncomingDrinkOrder(self, search_string):
        if self.lastclicktime is not None:
            if time.time() - self.lastclicktime < 2:
                logging.info("Ignoring rapid clicks")
                return
        self.lastclicktime = time.time()
        logging.info("Incoming DrinkOrder")
        
        # search for a recipe
        self.recipe = drinkprocessor.Recipe(search_string=search_string)

        # add an order to the order queue
        self.drinkprocessor.addOrder(self.recipe)

    def calling_reference_run(self):
        logging.info("Calling reference run")

        self.steppermotor.reference_run()

    def drink_in_progress(self):
        logging.info("Drink in progress")
        if self.drinkprocessor.drinkInProgress():
            self.root.current = "DrinkInProgress"
            logging.info("Drink in progress")
    


