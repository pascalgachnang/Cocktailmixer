import kivy
import logging
from kivy.app import App
from kivy.uix.widget import Widget  
from kivy.uix.button import Button  
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from StepperMotor.StepperMotor import StepperMotor

class MyGrid(GridLayout):
    def __init__(self, **kwargs):
        super(MyGrid, self).__init__(**kwargs)
        self.cols = 2
        self.add_widget(Label(text="First Name: "))
        self.name = TextInput(multiline=False)
        self.add_widget(self.name)

        self.add_widget(Label(text="Last Name: "))
        self.lastname = TextInput(multiline=False)
        self.add_widget(self.lastname)

        self.add_widget(Label(text="Email: "))
        self.email = TextInput(multiline=False)
        self.add_widget(self.email)

        self.submit = Button(text="Submit", font_size=40)
        self.submit.bind(on_press=self.pressed)
        self.add_widget(self.submit)
    
    def pressed(self, instance):
        name = self.name.text
        last = self.lastname.text
        email = self.email.text
        
        print("Name: {0}, Last Name: {1}, Email: {2}".format(name, last, email))
        
        self.name.text = ""
        self.lastname.text = ""
        self.email.text = ""
        
        self.add_widget(Label(text="Name: {0}, Last Name: {1}, Email: {2}".format(name, last, email)))

        self.CallStepperMotor(instance)    

    def CallStepperMotor(self, instance):
        logging.info("Calling StepperMotor")
        self.stepm = StepperMotor(800, 800)
        self.stepm.start()
        self.stepm.join()
        logging.info("Calling StepperMotor: {0}".format(self.stepm))
        #self.stepm._nema17_ramp(8000, 800)
        self.stepm.reference_run()

class MyVisualization(App):
    def build(self):
        return MyGrid()
    


