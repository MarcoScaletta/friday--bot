
import logging
import os
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
import config

import reply_options as reply


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    TOKEN = os.environ.get('ALFRED_BOT_TOKEN')
    updater = Updater(TOKEN, use_context=True)

    dp = updater.dispatcher
    replier = reply.Replier(dp)

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', replier.start), CommandHandler(
            'fermata', replier.ask_stop)],
        states={
            config.DEFAULT_STATE: [MessageHandler(Filters.text, replier.default), CommandHandler(
            'fermata', replier.ask_stop)],
            config.GTT_STOP: [MessageHandler(Filters.text, replier.reply_to_stop_number)]},
        fallbacks=[CommandHandler('start', replier.start), CommandHandler('cancel', replier.cancel)]
    )

    dp.add_handler(conv_handler)

    dp.add_error_handler(error)

    updater.start_polling()

    updater.idle()
            


if __name__ == '__main__':
    main()
