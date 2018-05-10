
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from vectorize_sentences import Mes2Vec
from data.data import clear_message
from random import randint


updater = Updater(token='MY_TOKEN')
dispatcher = updater.dispatcher
sticker_ids = ['CAADAgADAQADFgqsEHouQiu0Tr5WAg', 'CAADAgADBwADFgqsEA7M9oZNeed8Ag',
               'CAADAgADEQADFgqsEG1HufYsO4V5Ag', 'CAADAgADEAADFgqsELpgOnM_DpG7Ag',
               'CAADAgADFQADFgqsEFLrgRpOhlphAg', 'CAADBAADjAQAAsY_ZAWFy4Pje1d7uwI',
               'CAADBAADegQAAsY_ZAWk7WGNTDlmKgI', 'CAADBAADtAQAAsY_ZAVabSOrYYSmmwI',
               'CAADBAADBAUAAsY_ZAXaOdWMZTPf6gI', 'CAADBAADLggAAsY_ZAUwPrz5kv3YTQI',
               'CAADAgADRgIAAiCBFQABMX1nLcHbCRIC', 'CAADAgADTgIAAiCBFQABmcFR_vyclDcC',
               'CAADAgADXgIAAiCBFQAByI7ks8Gg9LAC', 'CAADAgADZgIAAiCBFQABU8uIJXg5VzgC',
               'CAADAQAD3QAD_QqQBPBu5mpVRbTvAg', 'CAADAQADMAEAAv0KkATFZWROq-cVRgI',
               'CAADAgADVgEAAsSraAsIwV4DAgM1agI', 'CAADAgADNAEAAsSraAsSav54wPzlQgI',
               'CAADAgADaAEAAsSraAvIKFzEIsyHQgI']


def start(bot, update):
    print('started bot')
    bot.send_message(chat_id=update.message.chat_id, text='Привет!')


def answer(bot, update):
    question = update.message.text
    response = m2v.throw_sentence(clear_message(question))
    bot.send_message(chat_id=update.message.chat_id, text=response)

def voice(bot, update):
    responds=['сорь, не могу послушать','ага, щаc бы на паре аудио слушать','блин, наушники не могу найти',
              'потом послушаю','я занята, не могу послушать']
    bot.send_message(chat_id=update.message.chat_id, text=responds[randint(0,len(responds) - 1)])


def location(bot, update):
    responds=['уже бегу к тебе','ну я ведь вссе равно потеряюсь','супер, там и встретимся']
    bot.send_message(chat_id=update.message.chat_id, text=responds[randint(0,len(responds) - 1)])


def photo(bot, update):
    responds=['но... у меня ведь нет глаз...','я пока не шарю в CNN и picture segmentation :(']
    bot.send_message(chat_id=update.message.chat_id, text=responds[randint(0,len(responds) - 1)])
    bot.send_sticker()


def document(bot, update):
    responds=['ты лучше просто поговори со мной','не, такое пока не спарщу, давай словами','я понимаю только русские слова','а можно словами?']
    bot.send_message(chat_id=update.message.chat_id, text=responds[randint(0,len(responds) - 1)])


def sticker(bot, update):
    bot.send_sticker(chat_id=update.message.chat_id, sticker=sticker_ids[randint(0,len(sticker_ids) - 1)])


if __name__ == '__main__':
    # Хендлеры
    start_command_handler = CommandHandler('start', start)
    text_message_handler = MessageHandler(Filters.text, answer)
    audio_message_handler = MessageHandler(Filters.voice, voice)

    # Добавляем хендлеры в диспетчер
    dispatcher.add_handler(start_command_handler)
    dispatcher.add_handler(text_message_handler)
    dispatcher.add_handler(audio_message_handler)
    dispatcher.add_handler(MessageHandler(Filters.document, document))
    dispatcher.add_handler(MessageHandler(Filters.location, location))
    dispatcher.add_handler(MessageHandler(Filters.photo, photo))
    dispatcher.add_handler(MessageHandler(Filters.sticker, sticker))

    # Начинаем поиск обновлений
    updater.start_polling(clean=True)
    m2v = Mes2Vec()
    # Останавливаем бота, если были нажаты Ctrl + C
    updater.idle()


