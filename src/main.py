# -*- coding: utf-8 -*-

# from telegram import ParseMode
from telegram import Updater, ChatAction, InlineQueryResultArticle
from globals import token, logger
import re
from howdoi.howdoi import howdoi as howdoi_call
from random import getrandbits


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


def escape_markdown(text):
    """Helper function to escape telegram markup symbols"""
    escape_chars = '\*_`\['
    return re.sub(r'([%s])' % escape_chars, r'\\\1', text)


def inlinequery(bot, update):
    result = ''
    _hex = hex(getrandbits(64))[2:]
    results = list()
    logger.info('Inline: ' + update.inline_query.query)
    if update.inline_query is not None and update.inline_query.query:
        query = update.inline_query.query.split(' ')
        result = howdoi(bot, update, query)
        results.append(
            InlineQueryResultArticle(
                id=_hex,
                title="StackOverflow",
                message_text="*%s*" % query,
                # parse_mode=ParseMode.MARKDOWN,
            )
        )

        bot.answerInlineQuery(update.inline_query.id, results=results)
    logger.debug('result=' + result)
    return results


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
    if 'inline_query' not in update.to_dict().keys():
        bot.sendMessage(chat_id, result)
    return result

if __name__ == '__main__':
    main()


def test():
    logger.info('Testing mode')
    from sys import argv
    from mock import Mock
    argv = argv[1:]
    bot = Mock()
    update = Mock()
    update.inline_query.query = argv
    update.to_dict().keys = Mock(return_value={'message': argv})
    result = howdoi(bot, update, argv)
    print(' ')
    print(result)
