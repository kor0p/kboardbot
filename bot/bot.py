import os
import logging

from telebot import TeleBot, logger


logger.setLevel(logging.DEBUG)


bot = TeleBot(os.environ['BOT_TOKEN'])
