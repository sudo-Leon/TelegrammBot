import telebot
from telebot import types


def choose_character(message, bot):
    """
    Отображает клавиатуру с выбором класса персонажа для пользователя.
    Эта клавиатура используется сразу после стартового сообщения,
    чтобы пользователь мог выбрать персонажа для начала игры.

    :param message: объект сообщения от пользователя
    :param bot: экземпляр бота
    """
    # Создаем клавиатуру для выбора персонажа
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    # Кнопки для выбора класса персонажа
    markup.add('Воин', 'Маг', 'Отшельник')
    # Отправка сообщения с предложением выбора класса персонажа
    bot.send_message(message.chat.id, "Выберите вашего персонажа:", reply_markup=markup)
