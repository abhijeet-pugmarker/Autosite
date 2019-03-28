#!/bin/bash

echo "Installing AutoSite....."
echo "Creating directory....."
mkdir ~/.autosite
echo "Moving files....."
sudo cp *.py ~/.autosite/
sudo chmod -R 755 ~/.autosite/

AUTOSITE='python3 ~/.autosite/app.py'
sudo echo -e "\n\nalias autosite='$AUTOSITE'" >> ~/.bashrc

echo "Autosite installed successfully."

