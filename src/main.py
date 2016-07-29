# -*- coding: utf-8 -*-

# from telegram import ParseMode
# from telegram.ext import Updater, InlineQueryHandler, CommandHandler
# from telegram import ChatAction, InlineQueryResultArticle
import telepot
from telepot.namedtuple import InlineQueryResultArticle, InputTextMessageContent
from telepot.delegate import per_chat_id, per_inline_from_id, create_open
from urllib3.exceptions import ReadTimeoutError

from globals import token, logger
from howdoi.howdoi import howdoi as howdoi_call
from howdoi.howdoi import _get_links
from random import getrandbits


class HowDoIBot(telepot.helper.InlineUserHandler, telepot.helper.AnswererMixin):
    """HowDoIBot"""

    def __init__(self, seed_tuple, timeout):
        super(HowDoIBot, self).__init__(seed_tuple, timeout)

    def on_chat_message(self, msg):
        content_type, chat_type, chat_id = telepot.glance(msg)

        if content_type != 'text':
            logger.info('{} message received'.format(content_type))
            return

        command = msg['text'].strip().lower()

        if ('/start' in command):
            self.start(msg)
        elif ('/howdoi' in command):
            self.howdoi(msg)
        else:
            logger.critical(msg)

    # Ignore group messages
    def on_edited_chat_message(self, msg):
        pass

    def escape_markdown(self, text):
        """Helper function to escape telegram markup symbols"""
        return '```{}```'.format(text)

    def howdoi(self, msg):
        content_type, chat_type, chat_id = telepot.glance(msg)
        msg['text'] = msg['text'].replace('/howdoi', '')
        logger.info("How do I received! [{}]".format(msg['text']))
        self.sender.sendChatAction('typing')
        args = {'all': True,
                'color': False,
                'num_answers': 1,
                'pos': 1,
                'query': msg['text']}
        try:
            result = howdoi_call(args)
            # result = self.escape_markdown(result)
        except ReadTimeoutError:
            result = 'Timeout finding some answer, sorry :('
        except Exception as e:
            logger.critical(e)
        self.sender.sendMessage(result)

    def start(self, msg):
        print(msg)
        self.sender.sendMessage("Hey *{}*!".format(
            msg['from']['first_name']), parse_mode='Markdown')

    def on_inline_query(self, msg):
        query_id, from_id, query_string = telepot.glance(
            msg, flavor='inline_query')
        logger.info('Inline ping from {}'.format(from_id))

        def compute_answer():
            link_results = _get_links(msg['query'])
            results = [w.split('/')[-1].replace('-', ' ')
                       for w in link_results]
            articles = [{'type': 'article',
                         'id': str(hex(getrandbits(64))[2:]),
                         'title': title,
                         'message_text': text}
                        for title, text in zip(results, link_results)]
            return articles

        self.answerer.answer(msg, compute_answer)

    def on_chosen_inline_result(self, msg):
        result_id, from_id, query_string = telepot.glance(
            msg, flavor='chosen_inline_result')
        print(self.id, ':', 'Chosen Inline Result:',
              result_id, from_id, query_string)


def test():
    logger.info('Testing mode')
    from sys import argv
    argv = argv[1:]
    args = {'all': False,
            'color': False,
            'num_answers': 1,
            'pos': 1,
            'query': argv}
    result = howdoi_call(args)
    print(' ')
    print(result)


def main():

    # Get the dispatcher to register handlers
    bot = telepot.DelegatorBot(token, [
        (per_inline_from_id(), create_open(HowDoIBot, timeout=30)),
        (per_chat_id(), create_open(HowDoIBot, timeout=10)),
    ])
    logger.info('Starting bot')
    # bot.message_loop({'inline_query': on_inline_query,
    #                   'chosen_inline_result': on_chosen_inline_result,
    #                   'chat': on_chat_message},
    #                  run_forever='Listening ...')
    bot.message_loop(run_forever='Listening ...')

if __name__ == '__main__':
    main()
