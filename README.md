# PyTel-Bot
A short bot in telegram
Made with Python-Telegram-Bot API (https://python-telegram-bot.org/) and Python 2.7.10
All methods and all the replies from the bot are in spanish.
## INTRODUCTION:    


This associate a COMMAND (/COMMAND in telegram chat) with a method (default_method). Is not necessary to
call the method, just is needed to make a reference.
```python
    updater.dispatcher.add_handler(CommandHandler('COMMAND', default_method)
```
For example, the command /start, is associated with BotActions.start
```python
    updater.dispatcher.add_handler(CommandHandler('start'), BotActions.start)
```
And, in your telegram chat, you'll see something like this:

```
    Hola, mundo!
```
The method random_file_name gives a random file name from a specific path. For example, if the path is full of images
it returns one random image name.
That is just a condition to avoid sending a .DS_Store file, you can make it with other files.
```python
    and f != '.DS_Store'
```

The parse_mode='Markdown' is for using a style in the message, for example, when using '__' for send an italic text.

```python
    bot.send_message(chat_id=chat_id, text='`' + str(chat_id) + '`', reply_to_message_id=update.message.message_id, parse_mode='Markdown')
```

The module telegram_tweet.py connects the telegram bot with @PyTwe_bot (http://www.github.com/alkesst/pytwe-bot).
The method new_tweet, post the tweet and returns the link where the tweet was posted.

All the methods' arguments are bot and update. With bot you can make actions like, sending messages, photos, etc...
With update you can get information of the message like the chat object, user object, etc...


## AUTOMATE THE BOT:

### Script:

To run the boot when turning on the raspberry we must create a service, that's easy to configure.

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
    python main.py

```


You will need to put this on your code, because the service will start immediatly when the rpi turns on, so, we need to
check if there is internet conection.
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

Made the script, now you need to create a .service file with this code:
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

### Enabling service and moving to the path:

When you have your .service file, you need to move the file into /etc/systemd/system/ and use this command:
```sh
    sudo systemctl enable pytwe.service
```

Spoiler: you will need to move first your service where you want and then use sudo mv pytwe_service /etc/systemd/system

Don't forget this:
```sh
    chmod a+x rpi_pytwe_script.sh
```

And now your bot will run when the rpi powers on.
