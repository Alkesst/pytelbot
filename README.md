# PyTel-Bot
###### A playful telegram bot.
## Requirements
Python3 or Docker. Not both!

## Introduction
A telegram bot that interacts with the users in telegram groups. It sends photos, videos 
and stickers.

##### _TOKENS_
The tokens are saved using environment variables:

| VARIABLE | DESCRIPTION |
|----------|--------------|
| `PYTEL_TELEGRAM` | Telegram API key |
| `PYTEL_CONSUMER_KEY` | Twitter Consumer Key |
| `PYTEL_CONSUMER_SECRET` | Twitter Consumer Secret |
| `PYTEL_ACCESS_TOKEN` | Twitter's user Access Token |
| `PYTEL_ACCES_TOKEN_SECRET` | Twitter's user Access Token Secret |
| `PYTEL_PATH` | Optional variable that points to where the files and database are stored |

## AUTOMATE THE BOT

### Using Docker
Before creating the image with docker, we need to create the .env with the next content:
```
PYTEL_TELEGRAM=*REPLACE WITH YOUR TOKEN*
PYTEL_CONSUMER_KEY=*REPLACE WITH YOUR TOKEN*
PYTEL_CONSUMER_SECRET=*REPLACE WITH YOUR TOKEN*
PYTEL_ACCESS_TOKEN=*REPLACE WITH YOUR TOKEN*
PYTEL_ACCES_TOKEN_SECRET=*REPLACE WITH YOUR TOKEN*
PYTEL_PATH=*REPLACE WITH YOUR CUSTOM PATH*
```

By default, PYTEL_PATH is equals to ../pytel_stuff
All the images you want to use will need to be in the docker image.

First create the image with `docker image build -t *tag_name* .` and will create an image from the Dockerfile.

Once created your image, just run with `docker run -it --rm -v *pytel_files_path*:/pytel_stuff --env-file .env *tag_name*`.


### Using Services
#### Script:

To run the bot when turning on the raspberry we must create a service.

First of all we need to create a script that pulls the changes from git, and then, runs the bot
```sh
#!/usr/bin/env bash
cd /home/pi/Documentos/PyTel-Bot # Path to where the source code is

#  ... SET THE TOKENS VARIABLES HERE ...
export PYTEL_TELEGRAM=*REPLACE WITH YOUR TOKEN*
export PYTEL_CONSUMER_KEY=*REPLACE WITH YOUR TOKEN*
export PYTEL_CONSUMER_SECRET=*REPLACE WITH YOUR TOKEN*
export PYTEL_ACCESS_TOKEN=*REPLACE WITH YOUR TOKEN*
export PYTEL_ACCES_TOKEN_SECRET=*REPLACE WITH YOUR TOKEN*
export PYTEL_PATH=*REPLACE WITH YOUR CUSTOM PATH*

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

#### Service:

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

#### Enabling service and moving to the path:

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
