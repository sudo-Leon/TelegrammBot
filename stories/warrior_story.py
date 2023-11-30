from telebot import types


def send_warrior_story(bot, message):
    """
    Отправляет пользователю предысторию воина и предоставляет выбор дальнейших действий.
    Каждое действие сопровождается инлайн-кнопкой, позволяющей пользователю принять решение.

    :param bot: экземпляр бота
    :param message: объект сообщения от пользователя
    """
    # Отправляем предысторию война
    bot.send_message(message.chat.id, "Вы великий воин, обладающий ...")

    # Создаем инлайн-клавиатуру с вариантами действий для война
    markup = types.InlineKeyboardMarkup(row_width=2)
    # Кнопки предлагают различные сценарии, которые воин может выбрать
    option1 = types.InlineKeyboardButton("1 - 🌲 Исследовать лес", callback_data="warrior_option_1")
    option2 = types.InlineKeyboardButton("2 - 🏙 Отправиться в город", callback_data="warrior_option_2")
    option3 = types.InlineKeyboardButton("3 - 👥 Поискать спутников", callback_data="warrior_option_3")
    markup.add(option1, option2, option3)

    # Отправляем сообщение с инлайн-клавиатурой для выбора пользователем
    bot.send_message(message.chat.id, "Как вы будете действовать?", reply_markup=markup)


def warrior_options_handler(bot, call):
    """
    Обрабатывает выбор пользователя после нажатия на инлайн-кнопку.
    Каждая кнопка соответствует определенному действию в сценарии воина.

    :param bot: экземпляр бота
    :param call: объект callback-запроса от нажатия кнопки
    """
    # Обработка выбора действия пользователя
    if call.data == "warrior_option_1":
        # Пользователь выбрал исследовать лес
        bot.send_message(call.message.chat.id, "Вы выбрали исследовать лес.")
    elif call.data == "warrior_option_2":
        # Пользователь выбрал отправиться в город
        bot.send_message(call.message.chat.id, "Вы отправились в город.")
    elif call.data == "warrior_option_3":
        # Пользователь выбрал поискать спутников
        bot.send_message(call.message.chat.id, "Вы решили поискать спутников.")
    # Отправляем подтверждение обработки callback-запроса
    bot.answer_callback_query(call.id)
