global logger
global bot
from telebot import TeleBot

import os
import logging
import logging.config

# load the logging configuration

real_path = os.path.dirname(os.path.realpath(__file__))
logging.config.fileConfig(real_path + '/logging.ini')
logger = logging.getLogger(__name__)

token = "TOKEN"
bot = TeleBot(token)
