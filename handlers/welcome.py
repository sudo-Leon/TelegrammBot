from telebot import types
from game.characters import choose_character


def send_welcome(bot, message):
    """
    Отправляет приветственное сообщение и отображает инлайн-клавиатуру с кнопкой "Start".
    Эта функция вызывается при команде /start, если она была вызвана без дополнительных параметров.

    :param bot: экземпляр бота
    :param message: объект сообщения от пользователя
    """
    welcome_text = "Добро пожаловать в игру RPG!"
    # Создаем инлайн-клавиатуру с одной кнопкой "Start"
    markup = types.InlineKeyboardMarkup()
    start_button = types.InlineKeyboardButton(text="Start", callback_data="start_game")
    markup.add(start_button)
    # Отправляем приветственное сообщение вместе с клавиатурой
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup)


def handle_start(bot, call):
    """
    Обрабатывает нажатие на кнопку "Start" инлайн-клавиатуры.
    Отправляет пользователю предысторию и предлагает выбрать персонажа с помощью клавиатуры.

    :param bot: экземпляр бота
    :param call: объект callback-запроса от нажатия кнопки
    """
    # Подтверждаем обработку callback-запроса
    bot.answer_callback_query(call.id)
    # Отправляем предысторию игры
    bot.send_message(call.message.chat.id, "Ваша предыстория... [Тут идет ваша предыстория...]")
    # Вызываем функцию для отображения клавиатуры выбора персонажа
    choose_character(call.message, bot)
