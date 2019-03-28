#!/bin/bash

echo "Installing AutoSite....."
echo "Creating directory....."
mkdir ~/.autosite
echo "Moving files....."
sudo cp *.py ~/.autosite/
echo "Setting Permission"
sudo chmod -R 755 ~/.autosite/

AUTOSITE='python3 ~/.autosite/app.py'
sudo echo -e "\n\nalias autosite='$AUTOSITE'" >> ~/.bashrc

