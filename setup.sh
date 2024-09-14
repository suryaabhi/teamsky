#!/bin/bash

echo -n "Turning on I2C..."
sudo raspi-config nonint do_i2c 0
echo "Done!"

echo "Installing Python packages..."
pip install -r requirements.txt --break-system-packages
echo "Installing Python packages: Done!"
