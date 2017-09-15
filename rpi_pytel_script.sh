#!/usr/bin/env bash
cd /home/pi/Documentos/PyTel-Bot
echo "Pulling PyTel-Bot..."
echo
git pull
echo
echo "Pull done..."
echo "Initializating PyTel-Bot..."
python main.py
