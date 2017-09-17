#!/usr/bin/env bash
cd /home/pi/Documentos/PyTel-Bot
STATE=$(ping -q -w 1 -c 1 `ip r | grep default | cut -d ' ' -f 3` > /dev/null && echo ok || echo error)
while [  $STATE == "error" ]; do
    #do a ping and check that its not a default message or change to grep for something else
    STATE=$(ping -q -w 1 -c 1 `ip r | grep default | cut -d ' ' -f 3` > /dev/null && echo ok || echo error)

    #sleep for 2 seconds and try again
    sleep 2
 done
echo "Pulling PyTel-Bot..."
echo
git pull
echo
echo "Pull done..."
echo "Initializating PyTel-Bot..."
echo
echo "Bot running"
python main.py
