
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters


updater = Updater(token='TOKEN')
dispatcher = updater.dispatcher


def start(bot, update):
    print('started bot')
    bot.send_message(chat_id=update.message.chat_id, text='Привет!')


def answere(bot, update):
    question = update.message.text
    print('got question {}'.format(question))
    # response = get_response(question)
    response = question
    bot.send_message(chat_id=update.message.chat_id, text=response)


if __name__ == '__main__':
    # Хендлеры
    start_command_handler = CommandHandler('start', start)
    text_message_handler = MessageHandler(Filters.text, answere)
    # Добавляем хендлеры в диспетчер
    dispatcher.add_handler(start_command_handler)
    dispatcher.add_handler(text_message_handler)
    # Начинаем поиск обновлений
    updater.start_polling(clean=True)
    # Останавливаем бота, если были нажаты Ctrl + C
    updater.idle()


