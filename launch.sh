#!/bin/bash

# Activate the virtual environment

which python

cd /home/pi/Cocktailmixer
pwd
activate() {
    . /home/pi/Cocktailmixer/mixingjenny-env/bin/activate
}
activate
which python

# Run the main script
python ./src/main.py
