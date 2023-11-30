import telebot
from handlers.welcome import send_welcome, handle_start
from game.characters import choose_character
from stories.warrior_story import send_warrior_story, warrior_options_handler

# ... Ваши другие импорты ...

TOKEN = "6408728793:AAHytP1UHzMveLGLCEFrV1YcI48xAO2qjw0"
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    """
    Обработчик команды /start.
    Если команда содержит параметры, запускается новая игра.
    В противном случае отправляется приветственное сообщение с кнопкой начала игры.
    """
    args = message.text.split()[1:]  # Аргументы после команды /start
    if args and args[0].lower() == 'startgame':
        start_new_game(message)  # Начало новой игры, если есть параметр startgame
    else:
        send_welcome(bot, message)  # Отправка приветственного сообщения, если параметров нет


@bot.callback_query_handler(func=lambda call: call.data == "start_game")
def callback_start(call):
    """
    Обработчик нажатия на кнопку "Start".
    Отправляет пользователю предысторию и предлагает выбрать персонажа.
    """
    handle_start(bot, call)  # Обработка начала игры


def start_new_game(message):
    """
    Запускает новую игру, отправляя сообщение и предоставляя выбор персонажа.
    """
    bot.send_message(message.chat.id, "Начинаем новое приключение!")
    choose_character(message, bot)  # Предложение выбрать персонажа для игры


@bot.message_handler(func=lambda message: message.text in ["Воин", "Маг", "Отшельник"])
def character_chosen(message):
    """
    Обработчик выбора персонажа.
    Отправляет сообщение о выборе и вызывает соответствующую функцию сценария.
    """
    chosen_character = message.text
    bot.send_message(message.chat.id, f"Вы выбрали {chosen_character}. Теперь ваше приключение начинается!")
    if chosen_character == "Воин":
        send_warrior_story(bot, message)  # Сценарий для воина
    elif chosen_character == "Маг":
        # Сценарий для мага (функция ещё не реализована)
        pass
    elif chosen_character == "Отшельник":
        # Сценарий для отшельника (функция ещё не реализована)
        pass


@bot.callback_query_handler(func=lambda call: call.data.startswith("warrior_option_"))
def handle_warrior_options(call):
    """
    Обработчик опций действий для воина после выбора персонажа.
    Вызывает функцию, которая обрабатывает выбранную опцию.
    """
    warrior_options_handler(bot, call)  # Обработка выбора опции воина


bot.polling(none_stop=True)
