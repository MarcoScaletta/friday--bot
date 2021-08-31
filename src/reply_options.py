
import telegram
import requests

from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import ConversationHandler

import config
import logger
import persistent
import GTT_stop_departures


STOP_NUMBERS = 0
LAST_STOP = 1


class Replier:

    def __init__(self, dp, bot):
        self.dp = dp
        self.messages = {STOP_NUMBERS: dict(), LAST_STOP: dict()}
        self.bot = bot

    def reply(self, update, message):
        self.save_chatID(update)
        logger.info("reply")
        update.message.reply_text(message)

    def start(self, update, context):
        self.save_chatID(update)
        """Send a message when the command /start is issued."""
        logger.info("start")
        reply_markup = telegram.ReplyKeyboardRemove()

        response = "Salve, sono Alfred, al suo servizio.\n"
        response += "Prema su /fermata per cercare gli arrivi a una fermata GTT."
        update.message.reply_text(response, reply_markup=reply_markup)
        return config.DEFAULT_STATE

    def default(self, update, context):
        """Echo the user message."""

        logger.info("default")
        response = "Come? Temo di non aver capito. Selezioni uno di questi comandi" + '\n\n'
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
        chatID = self.get_chat_ID(update)        
        logger.info(update.message)

        menu_options = [["1", "2", "3"], ["4", "5", "6"], [
            "7", "8", "9"], ["BACK", "0",  "DEL"], ["OK"]]

        keyboard = ReplyKeyboardMarkup(menu_options)


        response = "Inserisci il numero della fermata\n"
        response += "(usa il tastierino o inserisci un numero con prefisso \"/\": ad esempio /1000)\n"
        if persistent.exists_chatID(chatID):
            fav_stop = persistent.get_favorite_stop(chatID)
            if fav_stop != "NULL":
                response += "Fermata preferita: /" + fav_stop
            else:
                response += "Nessuna fermata preferita salvata"
        response += "\n"
        
        update.message.reply_text(response,  reply_markup=keyboard)

        return config.GTT_STOP_NUMBER

    def get_my_stops(self,update,context):
        logger.info("get_my_stops")
        chatID = update.message["chat"]["id"]
        if not persistent.exists_chatID(chatID):
            persistent.insert_chatID(chatID)
            update.message.reply_text('Nessuna fermata preferita impostata!\nPer impostare una nuova fermata preferita usa il comando /fermata inserisci la fermata e poi usa il comando /salva_fermata_preferita')
        return ConversationHandler.END

    def composing_stop_number(self, update, context):
        logger.info("composing_stop_number")

        self.save_chatID(update)
        chat_id = self.get_chat_ID(update)
        message = update.message.text

        if chat_id in self.messages[STOP_NUMBERS]:
            print(list(map(lambda x : str(x), self.messages[STOP_NUMBERS][chat_id])))

        if message[0] == "/":
            if chat_id in self.messages[STOP_NUMBERS]:
                self.messages[STOP_NUMBERS][chat_id].clear()
            try: 
                number = str(int(message[1:]))
                self.messages[LAST_STOP][chat_id] = number
                return self.reply_to_stop_number(update, context)
            except ValueError:
                update.message.reply_text(message[1:] +" non e' un numero di fermata, riprova.",
                                      reply_markup=ReplyKeyboardRemove())
        else:
            if message == "OK":
                number = ""
                if chat_id in self.messages[STOP_NUMBERS] and len(self.messages[STOP_NUMBERS][chat_id]) > 0:
                    for message in self.messages[STOP_NUMBERS][chat_id]:
                        number += str(message.text)
                        self.last_stop = number
                else:
                    self.reply(update, "Non hai inserito nessun numero, riprova.")
                    return None

                self.messages[STOP_NUMBERS][chat_id] = list()
                logger.info(number)
                self.messages[LAST_STOP][chat_id] = number
                return self.reply_to_stop_number(update, context)

            if message == "DEL":
                self.bot.deleteMessage(
                    chat_id, message_id=update.message.message_id)
                if chat_id in self.messages[STOP_NUMBERS] and len(self.messages[STOP_NUMBERS][chat_id]) > 0:
                    message = self.messages[STOP_NUMBERS][chat_id][-1]
                    self.messages[STOP_NUMBERS][chat_id] = self.messages[STOP_NUMBERS][chat_id][:-1]
                    self.bot.deleteMessage(chat_id, message_id=message.message_id)
            elif message == "BACK":
                update.message.reply_text("Ok, annullo \n\nPer fare un'altra ricerca /fermata",
                                        reply_markup=ReplyKeyboardRemove())
                if chat_id in self.messages[STOP_NUMBERS]:
                    self.messages[STOP_NUMBERS][chat_id].clear()
                return ConversationHandler.END
            elif chat_id not in self.messages[STOP_NUMBERS]:
                self.messages[STOP_NUMBERS][chat_id] = [update.message]
            else:
                self.messages[STOP_NUMBERS][chat_id].append(update.message)

        logger.info(message)

    def test_state_transition(self,update,context):
        print("TEST STATE ")


    def reply_to_stop_number(self, update, context):
        logger.info("reply_to_stop_number")
        chat_id = self.get_chat_ID(update)
        message = update.message.text
        self.save_chatID(update)
        stop_number = self.messages[LAST_STOP][chat_id]
        self.reply(update, str("Ricerca fermata numero " + stop_number + "..."))
        url = config.GTT_URL + stop_number + '/departures'
        logger.info(url)
        r = requests.get(url)
        if r.status_code == 404:
            self.reply(
                update, "Sembra che la fermata che hai inserito non esiste, riprova.")
            return config.GTT_STOP_NUMBER
        else:
            self.messages[LAST_STOP][chat_id] = stop_number
            response = "FERMATA " + stop_number + "\n"
            response += GTT_stop_departures.GTTStop.parse_departures(r.text)
            response += "\n\n"
            response += "Per fare un'altra ricerca /fermata\n"
            response += "Per salvare la fermata come preferita /salva_fermata\n"
            
            update.message.reply_text(response,
                                      reply_markup=ReplyKeyboardRemove())
        logger.info(r.text)
        return ConversationHandler.END

    def save_chatID(self, update):
        return None

    def save_stop(self, update, context):
        logger.info("save_stop")
        chatID = self.get_chat_ID(update)
        print(list(map(lambda x:str(x), self.messages[LAST_STOP])))
        if  chatID not in self.messages[LAST_STOP]:
            self.reply(update, "Non hai ancora effettuato alcuna ricerca:\nusa /fermata poi usa /salva_fermata per salvare la fermata")
        else:
            try:
                last_stop = self.messages[LAST_STOP][chatID]
                persistent.set_fav_stop(chatID, last_stop)
                self.reply(update, f"La fermata {last_stop} e'  stata salvata con successo")
            except Exception as e:
                self.reply(update, "Qualcosa non e' andato a buon fine, per favore riprova.")
                print(e)

    def get_chat_ID(self,update):
        logger.info("get_chat_ID")
        return str(update.message["chat"]["id"])

    def composing_stop_number_abs(self,update,context):
        logger.info("composing_stop_number_abs")
        self.composing_stop_number_concr(update,context, config.GTT_REPLY_NUMBER_REQ)

    def composing_stop_number_concr(self, update, context, nextState):
        logger.info("composing_stop_number_concr")
        self.save_chatID(update)
        chat_id = self.get_chat_ID(update)
        message = update.message.text

        if chat_id in self.messages[STOP_NUMBERS]:
            print(list(map(lambda x : str(x), self.messages[STOP_NUMBERS][chat_id])))
        print(f"message {message}")
        if message[0] == "/":
            print(f"\t==> {self.messages[LAST_STOP]}")
            if chat_id in self.messages[STOP_NUMBERS]:
                self.messages[STOP_NUMBERS][chat_id].clear()
            try: 
                number = str(int(message[1:]))
                self.messages[LAST_STOP][chat_id] = number
                print(f"\t==> {self.messages[LAST_STOP]}")
                return nextState
                # return self.reply_to_stop_number(update, context, number)
            except ValueError:
                update.message.reply_text(message[1:] +" non e' un numero di fermata, riprova.",
                                      reply_markup=ReplyKeyboardRemove())
        else:
            if message == "OK":
                number = ""
                if chat_id in self.messages[STOP_NUMBERS] and len(self.messages[STOP_NUMBERS][chat_id]) > 0:
                    for message in self.messages[STOP_NUMBERS][chat_id]:
                        number += str(message.text)
                        self.last_stop = number
                        self.messages[LAST_STOP][chat_id] = number
                else:
                    self.reply(update, "Non hai inserito nessun numero, riprova.")
                    # return None

                self.messages[STOP_NUMBERS][chat_id] = list()
                logger.info(number)
                self.messages[LAST_STOP][chat_id] = number
                print(f"before return {nextState}")
                return nextState
                # return self.reply_to_stop_number(update, context, number)

            if message == "DEL":
                self.bot.deleteMessage(
                    chat_id, message_id=update.message.message_id)
                if chat_id in self.messages[STOP_NUMBERS] and len(self.messages[STOP_NUMBERS][chat_id]) > 0:
                    message = self.messages[STOP_NUMBERS][chat_id][-1]
                    self.messages[STOP_NUMBERS][chat_id] = self.messages[STOP_NUMBERS][chat_id][:-1]
                    self.bot.deleteMessage(chat_id, message_id=message.message_id)
            elif message == "BACK":
                update.message.reply_text("Ok, annullo \n\nPer fare un'altra ricerca /fermata",
                                        reply_markup=ReplyKeyboardRemove())
                if chat_id in self.messages[STOP_NUMBERS]:
                    self.messages[STOP_NUMBERS][chat_id].clear()
                return ConversationHandler.END
            elif chat_id not in self.messages[STOP_NUMBERS]:
                self.messages[STOP_NUMBERS][chat_id] = [update.message]
            else:
                self.messages[STOP_NUMBERS][chat_id].append(update.message)

        logger.info(message)