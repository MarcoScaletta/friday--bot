
import logger
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
import config
import persistent

import reply_options as reply


def error(update, context):
    """Log Errors caused by Updates."""
    logger.error('Update "%s" caused error "%s"', update, context.error)


def main():

    logger.info("Started")
    if not logger.is_set_log_option():
        logger.warning("no log option set", log_anyway=True)
    
    print(config.TOKEN)
    updater = Updater(config.TOKEN, use_context=True)
    bot = telegram.bot.Bot(config.TOKEN)
    

    dp = updater.dispatcher
    
    replier = reply.Replier(dp, bot)


    conv_handler = ConversationHandler(
        
        entry_points=[
            CommandHandler('start', replier.start), 
            CommandHandler('fermata', replier.ask_stop),
            CommandHandler('salva_fermata', replier.save_stop),
            ],
        
        states={
            
            config.DEFAULT_STATE: [
                CommandHandler('fermata', replier.ask_stop),
                MessageHandler(Filters.text, replier.default)],
            config.GTT_REPLY_NUMBER_REQ: [
                MessageHandler(Filters.text, replier.test_state_transition)
                ],
            config.GTT_STOP_NUMBER: [
                MessageHandler(Filters.text, replier.composing_stop_number_abs)
                ],
            },
        
        fallbacks=[
            CommandHandler('start', replier.start),
            CommandHandler('fermata', replier.ask_stop),
            ]
    )

    dp.add_handler(conv_handler)

    dp.add_error_handler(error)

    updater.start_polling()

    updater.idle()

    logger.info("Stopped")


if __name__ == '__main__':
    main()
