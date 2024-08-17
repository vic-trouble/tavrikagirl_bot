import telebot
from telebot.custom_filters import IsReplyFilter
import re
import logging

logging.basicConfig(level=logging.DEBUG)

TARGET_CHAT_ID = 1054639124  # vic: 946013950
TOKEN = os.getenv("TG_TOKEN")
bot = telebot.TeleBot(TOKEN, parse_mode=None) # You can set parse_mode by default. HTML or MARKDOWN

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Привет!")

@bot.message_handler(is_reply=True)
def reply_from_polly(message):
    m = re.match('.*\\n\\n#id([-0-9]+)', message)
    if m:
        reply_id = m.group(1)
        bot.copy_message(chat_id=reply_id, from_chat_id=message.chat_id, message_id=message.id)
    
@bot.message_handler(func=lambda m: True)
def send_to_polly(message):
    bot.send_message(TARGET_CHAT_ID, message.text + f'\n\n#id{message.chat.id}')


if __name__ == '__main__':
    bot.add_custom_filter(IsReplyFilter())
    bot.infinity_polling()
