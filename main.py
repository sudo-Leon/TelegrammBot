import telebot
from telebot import types
from handlers.welcome import send_welcome, handle_start
from game.characters import choose_character
from stories.warrior_story import send_warrior_story, warrior_options_handler
from stories.character.warrior_character import Warrior

# ... Ваши другие импорты ...

# Глобальный словарь для хранения информации о персонажах пользователей
user_characters = {}

TOKEN = "6408728793:AAHytP1UHzMveLGLCEFrV1YcI48xAO2qjw0"
bot = telebot.TeleBot(TOKEN)


# Обработчик для текста кнопки "ID Героя"
@bot.message_handler(func=lambda message: message.text == "ID Героя")
def handle_id_button(message):
    send_id(message)


# Обработчик для текста кнопки "Карта"
@bot.message_handler(func=lambda message: message.text == "Карта")
def handle_map_button(message):
    send_map(message)


# Функция для создания основного меню после выбора персонажа
def main_menu(message):
    """
    Создает и отправляет пользовательскую клавиатуру с основными опциями игры.
    """
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    character_info_button = types.KeyboardButton('ID Героя')
    map_button = types.KeyboardButton('Карта')
    markup.add(character_info_button, map_button)
    bot.send_message(message.chat.id, "Выберите опцию:", reply_markup=markup)


# Обработчик для команды /id, который отправляет информацию о персонаже
@bot.message_handler(commands=['id'])
def send_id(message):
    user_id = message.from_user.id
    # Проверяем, есть ли персонаж для пользователя
    if user_id in user_characters:
        # Отправляем информацию о персонаже
        send_character_info(message, user_characters[user_id])
    else:
        # Если персонаж не найден, отправляем сообщение об ошибке
        bot.send_message(message.chat.id, "Персонаж не найден. Начните новую игру.")

# Обработчик для команды /map
@bot.message_handler(commands=['map'])
def send_map(message):
    """
    Отправляет карту мира или информацию о местоположении персонажа.
    """
    # Здесь должен быть код для отправки карты мира или местоположения
    bot.send_message(message.chat.id, "Карта мира пока недоступна.")


# Добавляем обработчик команды /newgame
@bot.message_handler(commands=['newgame'])
def new_game(message):
    """
    Позволяет пользователю начать новую игру, сбрасывая любое предыдущее состояние.
    """
    # Тут можно добавить логику сброса состояния игры, если она будет реализована
    # Например: reset_game_state(user_id)

    # Отправляем сообщение о начале новой игры и предлагаем выбрать персонажа
    bot.send_message(message.chat.id, "Вы начали новую игру! Выберите вашего персонажа:")
    choose_character(message, bot)


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
        # Запросите имя воина у пользователя
        bot.send_message(message.chat.id, "Введите имя воина:")
        bot.register_next_step_handler(message, create_warrior)
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


def create_warrior(message):
    """
    Создает объект воина с введенным пользователем именем и выводит информацию о нем.
    """
    warrior_name = message.text
    # Создаем объект воина с заданными характеристиками
    warrior = Warrior(name=warrior_name)
    # Сохраняем объект воина в глобальный словарь, используя ID пользователя как ключ
    user_characters[message.from_user.id] = warrior
    # Отправляем информацию о воине пользователю
    send_character_info(message, warrior)
    # Переход к следующему этапу сценария воина

    main_menu(message)  # Отображаем основное меню


# Функция для отправки информации о персонаже
def send_character_info(message, character):
    info = (f"Имя: {character.name}\n"
            f"Тип: Воин\n"
            f"Здоровье: {character.health}\n"
            f"Урон: {character.damage}\n"
            f"Сила: {character.strength}\n"
            f"Ловкость: {character.agility}\n"
            f"Выносливость: {character.endurance}\n"
            f"Способность: {character.class_ability}")
    bot.send_message(message.chat.id, info)


bot.polling(none_stop=True)
