
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from vectorize_sentences import Mes2Vec
from datasets.twitter.data import clear_message
from random import randint


updater = Updater(token='494392101:AAGM1SLC5ImvjzdYiWQpwgWq54NjpdzbsMg')
dispatcher = updater.dispatcher


def start(bot, update):
    print('started bot')
    bot.send_message(chat_id=update.message.chat_id, text='Привет!')


def answere(bot, update):
    question = update.message.text
    response = m2v.throw_sentence(clear_message(question))
    bot.send_message(chat_id=update.message.chat_id, text=response)

def audio(bot, update):
    print("got audio")
    responds=['сорь, не могу послушать','ага, щаз бы на паре аудио слушать','блин, наушники не могу найти','потом послушаю','я занята, не могу послушать']
    bot.send_message(chat_id=update.message.chat_id, text=responds[randint(0,len(responds) - 1)])


if __name__ == '__main__':
    # Хендлеры
    start_command_handler = CommandHandler('start', start)
    text_message_handler = MessageHandler(Filters.text, answere)
    audio_message_handler = MessageHandler(Filters.voice, audio)
    # Добавляем хендлеры в диспетчер
    dispatcher.add_handler(start_command_handler)
    dispatcher.add_handler(text_message_handler)
    dispatcher.add_handler(audio_message_handler)

    # Начинаем поиск обновлений
    updater.start_polling(clean=True)
    m2v = Mes2Vec()
    # Останавливаем бота, если были нажаты Ctrl + C
    updater.idle()


