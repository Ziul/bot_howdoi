# -*- coding: utf-8 -*-

import os
import logging
import logging.config
from telegram import Updater, Update, InlineQueryResultPhoto, ParseMode, InlineQueryResultArticle
from globals import *


def main():
    # load the logging configuration

    real_path = os.path.dirname(os.path.realpath(__file__))
    logging.config.fileConfig(real_path + '/logging.ini')
    logger = logging.getLogger(__name__)

    # Get the dispatcher to register handlers
    token = "162832990:AAEDSmIAFyeNptEVYgd9a8qBnh-E8J-nT5s"
    updater = Updater(token=token)
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.addTelegramCommandHandler("start", start)

    # log all errors
    dp.addErrorHandler(error)

    logger.info('Starting new bot')
    # Start the Bot
    updater.start_polling()

    # Block until the you presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


def start(bot, update, args):
    chat_id = update.message.chat_id
    bot.sendMessage(chat_id, "Hey!")


def error(bot, update, error):
    logger.critical('Update "%s" caused error "%s"' % (update, error))
    chat_id = update.message.chat_id
    bot.sendMessage(chat_id, text='Sorry {}, but {}'.format(
        update.first_name, error))


def inlinequery(bot, update):
    if update.inline_query is not None and update.inline_query.query:
        api = "https://api.deckbrew.com/mtg/cards/typeahead?q=<NAME>"
        query = update.inline_query.query.split("//")[0].strip()
        logger.debug("Query is :{0}".format(query))
        cards = requests.get(api.replace(
            "<NAME>", query.lower().replace(",", "")).replace("'", "")).json()
        images = list()
        i = 0
        if(cards == []):
            return
        if (len(cards) == 1):
            images.append(InlineQueryResultPhoto(id=hex(getrandbits(64))[2:],
                                                 photo_url=cards[0]['editions'][
                                                     0]['image_url'],
                                                 thumb_url=cards[0]['editions'][0]['image_url']))
            logger.debug("Card {0} : {1}".format(
                cards[0]['name'], cards[0]['editions'][0]['image_url']))
            bot.answerInlineQuery(update.inline_query.id, results=images)
            return
        for card in cards:
            img = ''
            if(card['editions'][0]['multiverse_id'] == 0):
                img = card['editions'][1]['image_url']
            else:
                img = card['editions'][0]['image_url']
            images.append(InlineQueryResultPhoto(id=i, caption=card['name'],
                                                 title=card['name'],
                                                 photo_url=img,
                                                 thumb_url=img))
            logger.debug("Card {0} {1} : {2}".format(i, card['name'], img))
            i = i + 1
        bot.answerInlineQuery(update.inline_query.id, results=images)

if __name__ == '__main__':
    main()
