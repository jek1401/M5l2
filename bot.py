import telebot
from config import *
from logic import *

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, "Привет! Я бот, который может показывать города на карте. Напиши /help для списка команд.")

@bot.message_handler(commands=['help'])
def handle_help(message):
    bot.send_message(message.chat.id, "Доступные команды:\n"
                                  "/show_city <город> - Показать город на карте\n"
                                  "/remember_city <город> - Запомнить город\n"
                                  "/show_my_cities - Показать сохраненные города")

@bot.message_handler(commands=['show_city'])
def handle_show_city(message):
    city_name = ' '.join(message.text.split()[1:])
    if not city_name:
        bot.send_message(message.chat.id, "Введите название города после команды.")
        return
    
    coordinates = manager.get_coordinates(city_name)
    if coordinates:
        image_path = f"{city_name}.png"
        manager.create_graph(image_path, [city_name])
        with open(image_path, 'rb') as photo:
            bot.send_photo(message.chat.id, photo)
    else:
        bot.send_message(message.chat.id, "Город не найден в базе данных.")

@bot.message_handler(commands=['remember_city'])
def handle_remember_city(message):
    user_id = message.chat.id
    city_name = ' '.join(message.text.split()[1:])
    if manager.add_city(user_id, city_name):
        bot.send_message(message.chat.id, f'Город {city_name} успешно сохранен!')
    else:
        bot.send_message(message.chat.id, 'Такого города я не знаю. Убедитесь, что он написан на английском!')

@bot.message_handler(commands=['show_my_cities'])
def handle_show_visited_cities(message):
    cities = manager.select_cities(message.chat.id)
    if cities:
        image_path = "my_cities.png"
        manager.create_graph(image_path, cities)
        with open(image_path, 'rb') as photo:
            bot.send_photo(message.chat.id, photo)
    else:
        bot.send_message(message.chat.id, "Вы не сохранили ни одного города.")

if __name__ == "__main__":
    manager = DB_Map(DATABASE)
    bot.polling()