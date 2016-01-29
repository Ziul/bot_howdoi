# Bot to *How-do-i*

[![Build Status](https://travis-ci.org/Ziul/bot_howdoi.svg?branch=master)](https://travis-ci.org/Ziul/bot_howdoi)

Bot to Telegram that parser the input to `howdoi` package.

More about it [here](https://github.com/gleitz/howdoi/).

# How to use on Telegram

Include the user ` @how_do_i_bot` into the chat or click [here](https://telegram.me/how_do_i_bot) to start chatting.

# How to replicate the bot

Install the bot with:

    pip install -e .
    
Into the file [globals.py](src/globals.py), inset the private token to the bot. 
Then run the bot with:

    bot-run
    
The bot should start running.
