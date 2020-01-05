import telegram
import requests
import config
import logger
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove,
                      InlineKeyboardButton, InlineKeyboardMarkup)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler)
import GTT_stop_departures


STOP_NUMBERS = 0


class Replier:

    def __init__(self, dp, bot):
        self.dp = dp
        self.messages = {STOP_NUMBERS: dict()}
        self.bot = bot

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
        logger.info(update.message)

        menu_options = [["1","2","3"], ["4","5","6"], ["7","8","9"], ["DEL","0","OK"]]

        keyboard = ReplyKeyboardMarkup(menu_options)

        update.message.reply_text(
            'Numero della fermata\n__(premere/scrivere **OK** una volta finito)__', parse_mode="Markdown", reply_markup=keyboard)
        return config.GTT_STOP_NUMBER

    def composing_stop_number(self, update, context):
        chat_id = update.message.chat_id
        message = update.message.text
        if message == "OK":
            number = ""
            for message in self.messages[STOP_NUMBERS][chat_id]:
                number += str(message.text)
            self.messages[STOP_NUMBERS][chat_id] = list()
            logger.info(number)
            return self.reply_to_stop_number(update, context, number)

        if message == "DEL":
            self.bot.deleteMessage(
                chat_id, message_id=update.message.message_id)
            if chat_id in self.messages[STOP_NUMBERS] and len(self.messages[STOP_NUMBERS][chat_id]) > 0:
                message = self.messages[STOP_NUMBERS][chat_id][-1]
                self.messages[STOP_NUMBERS][chat_id] = self.messages[STOP_NUMBERS][chat_id][:-1]
                self.bot.deleteMessage(chat_id, message_id=message.message_id)
        elif chat_id not in self.messages[STOP_NUMBERS]:
            self.messages[STOP_NUMBERS][chat_id] = [update.message]
        else:
            self.messages[STOP_NUMBERS][chat_id].append(update.message)

        logger.info(message)
        menu_options = [
            [telegram.KeyboardButton(1)]
        ]
        keyboard = ReplyKeyboardMarkup(menu_options)

    def reply_to_stop_number(self, update, context, number):
        stop_number = number
        self.reply(update, str("Ricerca fermata numero " + stop_number + "..."))
        url = config.GTT_URL + stop_number + '/departures'
        logger.info(url)
        logger.info('Send request to %s', url)
        r = requests.get(url)
        if r.status_code == 404:
            self.reply(
                update, "Sembra che la fermata che hai inserito non esiste, riprova.")
            return config.GTT_STOP_NUMBER
        else:
            response = "FERMATA " + stop_number + "\n"
            response += GTT_stop_departures.GTTStop.parse_departures(r.text)
            update.message.reply_text(
                response, reply_markup=ReplyKeyboardRemove())
        logger.info(r.text)
        return config.DEFAULT_STATE
