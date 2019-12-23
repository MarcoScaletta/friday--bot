
import telegram
import os
print("hi")
TOKEN = os.environ.get('FRIDAY_BOT_TOKEN')
bot = telegram.Bot(token=TOKEN)
print(bot.get_me())
