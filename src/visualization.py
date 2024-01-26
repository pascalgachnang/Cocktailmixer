import kivy
import logging
from kivy.app import App
from kivy.uix.widget import Widget  
from kivy.uix.button import Button  
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from StepperMotor.StepperMotor import StepperMotor
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder


class PasswordWindow(Screen):
    pass

class PositioningWindow(Screen):
    pass

class MainWindow1(Screen):
    pass

class MainWindow2(Screen):
    pass

class WindowManager(ScreenManager):
    pass


kv = Builder.load_file("my.kv")

    

class MyMainApp(App):
    def build(self):
        return kv 
    


