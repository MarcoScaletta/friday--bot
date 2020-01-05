import telegram
import requests
import config
import logger
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler)
import GTT_stop_departures


class Replier:
    
    def __init__(self, dp):
        self.dp = dp

    def reply(self, update, message):
        logger.info("reply")
        update.message.reply_text(message)

    def start(self, update, context):
        """Send a message when the command /start is issued."""
        logger.info("start")
        reply_markup = telegram.ReplyKeyboardRemove()
        update.message.reply_text('Hi, welcome!', reply_markup=reply_markup)
        return config.DEFAULT_STATE

    # def help(self, update, context):
    #     """Send a message when the command /help is issued."""
    #     update.message.reply_text(
    #         'Hi, it seems that you need help.\nI\'m sorry, but I don\'t know what to do.')

    def default(self, update, context):
        """Echo the user message."""
        logger.info("default")
        response = "Cosa? Non ho capito. Prova con questi comandi" + '\n\n'
        response += "- /fermata"
        update.message.reply_text(response)
        
    def cancel(self, update, context):
        logger.info("cancel")
        user = update.message.from_user
        update.message.reply_text('Bye! I hope we can talk again some day.',
                                reply_markup=ReplyKeyboardRemove())
        return config.DEFAULT_STATE

    def ask_stop(self, update, context):
        logger.info("ask_stop")
        self.reply(update, "Numero della fermata?")
        return config.GTT_STOP

    def reply_to_stop_number(self, update, context):
        stop_number = update.message.text
        self.reply(update, str("Ricerca fermata numero " + stop_number + "..."))
        url = config.GTT_URL + stop_number + '/departures'
        logger.info(url)
        # logger.log('Send request to %s', url)
        r = requests.get(url)
        if r.status_code == 404:
            self.reply(update, "Sembra che la fermata che hai inserito non esiste, riprova.")
            return config.GTT_STOP
        else:
            response = "FERMATA " + stop_number + "\n"
            response += GTT_stop_departures.GTTStop.parse_departures(r.text)
            self.reply(update, response)
        logger.info(r.text)
        return config.DEFAULT_STATE

    
