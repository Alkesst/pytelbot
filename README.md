# PyTel-Bot
###### A playful telegram bot.
## Requirements
- Python 3.x
- Tweepy
- Python-Telegram-Bot

## Introduction
A telegram bot that interacts with the users in telegram groups. It sends photos, videos 
and stickers.
 
##### _JSON's_
Pytel works with JSON's. The tokens are placed into tokens.json, and the main file
will read whole tokens that allows access to the telegram and twitter apis.

Also, ids.json contains the telegram users ids from the users you want allow to 
use the /tweet feature. 

Furthermore, each time a user makes use of the /tweet feature, it will be printed
into a log with the content of the tweet, the user who posted that tweet and the date when
it was posted.


## AUTOMATE THE BOT

### Script:

To run the bot when turning on the raspberry we must create a service.

First of all we need to create a script that pulls the changes from git, and then, runs the bot
```sh
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
    python3 main.py

```


It is requiered to use the following code, because the service will start immediatly when the rpi turns on, so, we need to
check if there is internet conection before trying to pull from git.
```sh
STATE=$(ping -q -w 1 -c 1 `ip r | grep default | cut -d ' ' -f 3` > /dev/null && echo ok || echo error)
while [  $STATE == "error" ]; do
    #do a ping and check that its not a default message or change to grep for something else
    STATE=$(ping -q -w 1 -c 1 `ip r | grep default | cut -d ' ' -f 3` > /dev/null && echo ok || echo error)

    #sleep for 2 seconds and try again
    sleep 2
 done
```

### Service:

Made the script, now you need to create a .service file with the following code:
```
[Unit]
Description=PyTwe-Bot

[Service]
ExecStart=/home/pi/rpi_pytwe_script.sh
User=pi
Group=pi

[Install]
WantedBy=multi-user.target

```

### Enabling service and moving to the path:

When you have your .service file, you need to move the file into /etc/systemd/system/ and use the following command:
```sh
    sudo systemctl enable pytwe.service
```

Spoiler: you will need to move first your service where you want and then use *__sudo mv pytwe_service /etc/systemd/system__*

Don't forget this:
```sh
    chmod a+x rpi_pytwe_script.sh
```

And now your bot will run when the rpi powers on.
