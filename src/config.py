import configparser
import os


# Load the config file and makes it available as a global variable
config_folder = 'config'
config_file = os.path.join(config_folder, 'config.ini')
config = configparser.ConfigParser()
config.read(config_file)