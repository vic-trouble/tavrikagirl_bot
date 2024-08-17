import logging
import os
import re

import telebot
from telebot.custom_filters import IsReplyFilter

logging.basicConfig(level=logging.DEBUG)

TARGET_CHAT_ID = 946013950
TOKEN = os.getenv("TG_TOKEN")
bot = telebot.TeleBot(TOKEN, parse_mode=None) # You can set parse_mode by default. HTML or MARKDOWN


def compose(text, chat_id):
    return f'{text}\n\n#id{chat_id}'


def extract_chat_id(text):
    last_line = text.split('\n')[-1].strip()
    logging.info('last line: %s', last_line)
    m = re.match('#id([0-9]+)', last_line)
    return m.group(1) if m else None


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет!")


@bot.message_handler(is_reply=True)
def reply_from_polly(message):
    reply_id = extract_chat_id(message.reply_to_message.text)
    if reply_id:
        bot.copy_message(chat_id=reply_id, from_chat_id=message.chat.id, message_id=message.id)
    else:
        logging.warning('can\'t parse reply id from %s', message.reply_to_message.text)
    

@bot.message_handler(func=lambda m: True)
def send_to_polly(message):
    bot.send_message(TARGET_CHAT_ID, message.text + f'\n\n#id{message.chat.id}')


if __name__ == '__main__':
    bot.add_custom_filter(IsReplyFilter())
    bot.infinity_polling()
