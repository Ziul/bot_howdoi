# -*- coding: utf-8 -*-

# from telegram import Updater, Update,
# InlineQueryResultPhoto, ParseMode, InlineQueryResultArticle
from telegram import Updater, InlineQueryResultPhoto, ChatAction
from globals import *
from howdoi.howdoi import howdoi as howdoi_call


def main():

    # Get the dispatcher to register handlers
    updater = Updater(token=token)
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.addTelegramCommandHandler("start", start)
    dp.addTelegramCommandHandler("howdoi", howdoi)
    dp.addTelegramInlineHandler(inlinequery)

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
    logger.info('Inline query')
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
            images.append(InlineQueryResultPhoto(
                id=hex(getrandbits(64))[2:], photo_url=cards[
                    0]['editions'][0]['image_url'],
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


def howdoi(bot, update, args):
    logger.info("How do I received! [{}]".format(args))
    chat_id = update.message.chat_id
    bot.sendChatAction(chat_id, action=ChatAction.TYPING)
    args = {'all': False,
            'color': False,
            'num_answers': 1,
            'pos': 1,
            'query': args}
    result = howdoi_call(args).encode('utf-8', 'ignore')
    logger.debug(result)
    bot.sendMessage(chat_id, result)

if __name__ == '__main__':
    main()


def test():
    from sys import argv
    argv = argv[1:]
    args = {'all': False,
            'color': False,
            'num_answers': 1,
            'pos': 1,
            'query': argv}
    result = howdoi_call(args).encode('utf-8', 'ignore')
    print result
