import os
import telebot
from dotenv import dotenv_values

from svg_generator import generate_svg_for_dep_dict


def launch_bot():
    """
    Telegram bot launch
    :return:
    """
    config = dotenv_values(r".env")
    bot = telebot.TeleBot(config.get('TG_TOKEN'), parse_mode=None)

    @bot.message_handler(commands=['start', 'help'])
    def send_welcome(message):
        bot.reply_to(message,
                     "Напишите текст на французском, чтобы получить схему синтаксических зависимостей слов во входящих в него предложениях.")

    @bot.message_handler(content_types=['text'])
    def message_reply(message):
        """
        Calls pic generation function, deletes pictures from FS after sending to user
        """
        text = message.text
        chat_id = message.chat.id
        img_filenames = generate_svg_for_dep_dict(text, 25)
        for img_fn in img_filenames:
            with open(img_fn, 'rb') as img:
                bot.send_photo(chat_id, img)
            os.remove(os.path.splitext(img_fn)[0] + '.svg')
            os.remove(img_fn)

    bot.infinity_polling()


if __name__ == '__main__':
    launch_bot()
