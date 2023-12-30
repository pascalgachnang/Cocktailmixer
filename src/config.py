import configparser
import os
import json


# Load the config file and makes it available as a global variable
config_folder = 'config'
config_file = os.path.join(config_folder, 'config.ini')
config = configparser.ConfigParser()
config.read(config_file)


# Load the recipes from the JSON file and makes it available as a global variable
with open(os.path.join(config['Recipes']['recipes_path'], config['Recipes']['recipes_file'])) as file:
    recipes = json.load(file)
