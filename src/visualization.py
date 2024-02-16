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

    def cancel_pressed(self):
        if self.ids.progress_bar.value == 100:
            popup = Popup(title='Progress complete',
                          content=Label(text='Progress complete.'),
                          size_hint=(None, None), size=(300, 200))
            popup.open()

class WindowManager(ScreenManager):
    pass

# Load the kv file
kv = Builder.load_file("my.kv")

class MyCocktailmixerApp(App):
    def build(self):
        self.drinkprocessor = drinkprocessor.OrderQueue()
        self.drinkprocessor.start()
        self.lastclicktime = None
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

    


