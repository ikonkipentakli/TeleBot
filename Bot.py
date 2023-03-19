import random
import telebot
import requests
from telebot import types
from bs4 import BeautifulSoup as b

URL = 'https://www.anekdot.ru/last/good'

def parser(url):
    r = requests.get(url)
    soup = b(r.text, 'html.parser')
    anecdots = soup.find_all('div', class_='text')
    return [c.text for c in anecdots]

list_of_jokes = parser(URL)
random.shuffle(list_of_jokes)
#print(list_of_jokes)

bot = telebot.TeleBot('6061314193:AAGFmHUnFxYCFqGinNKvbCZtxMrKTVL7phg')

@bot.message_handler(commands=['start'])
def start(message):
    mess = f'Привет, <b>{message.from_user.first_name}</b>'
    bot.send_message(message.chat.id, mess, parse_mode='html')

@bot.message_handler(commands=['photo'])
def get_user_photo(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=4)
    item1 = types.KeyboardButton('1')
    item2 = types.KeyboardButton('2')
    item3 = types.KeyboardButton('3')
    item4 = types.KeyboardButton('4')

    markup.add(item1, item2, item3, item4)

    bot.send_message(message.chat.id, 'Выбери фото', reply_markup=markup)

@bot.message_handler()
def get_user_text(message):
    if message.text.lower() == 'hello':
        bot.send_message(message.chat.id, 'И тебе привет!', parse_mode='html')
    elif message.text.lower() == 'id':
        bot.send_message(message.chat.id, f'Твой ID: {message.from_user.id}', parse_mode='html')
    elif message.text.lower() == 'info':
        bot.send_message(message.chat.id, message, parse_mode='html')
    elif message.text.isdigit():
        photo = open (f'photos\\{int(message.text)}.jpg', 'rb')
        bot.send_photo(message.chat.id, photo)
    elif message.text.lower() == 'joke':
        bot.send_message(message.chat.id, list_of_jokes[0])
        del list_of_jokes[0]
    else:
        bot.send_message(message.chat.id, 'Не понял', parse_mode='html')


bot.polling(non_stop=True)