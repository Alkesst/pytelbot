# PyTel-Bot
A short bot in telegram
Made with Python-Telegram-Bot API (https://python-telegram-bot.org/) and Python 2.7.10
All methods and all the replies from the bot are in spanish.

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
