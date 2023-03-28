import random
import telebot
import requests
import openai
import json
from telebot import types
from bs4 import BeautifulSoup as b
from settings import OPEN_AI, BOT_VLAD

bot = telebot.TeleBot(BOT_VLAD)
openai.api_key = OPEN_AI

URL_PIC = "https://api.thecatapi.com/v1/images/search"

URL_JOKE = 'https://www.anekdot.ru/last/good'

def parser_joke(url):
    r = requests.get(url)
    soup = b(r.text, 'html.parser')
    anecdots = soup.find_all('div', class_='text')
    return [c.text for c in anecdots]

list_of_jokes = parser_joke(URL_JOKE)
random.shuffle(list_of_jokes)

def parser_pic(url):
    r = requests.get(url)
    obj = json.loads(r.text)
    img = obj[0]['url']
    return img

@bot.message_handler(commands=['start'])
def start(message):
    mess = f'Привет, <b>{message.from_user.first_name}</b>. Если хочешь шутку или картинку котика - напиши /меню. Если хочешь просто пообщаться, то задай вопрос'
    bot.send_message(message.chat.id, mess, parse_mode='html')

@bot.message_handler(commands=['chat'])
def chat(message):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=message.text,
        temperature=0.5,
        max_tokens=1000,
        top_p=1.0,
        frequency_penalty=0.5,
        presence_penalty=0.0,
    )
    try:
        bot.send_message(message.chat.id, response['choices'][0]['text'])
    except:
        print('Попробуй снова')

    
@bot.message_handler(commands=['меню'])
def get_user_menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=4)
    item1 = types.KeyboardButton('Котик')
    item2 = types.KeyboardButton('Шутка')
    item3 = types.KeyboardButton('Погода')
    item4 = types.KeyboardButton('Курсы')

    markup.add(item1, item2)

    bot.send_message(message.chat.id, 'Выбери опцию', reply_markup=markup)

@bot.message_handler()
def get_user_text(message):
    if message.text.lower() == 'hello':
        bot.send_message(message.chat.id, 'И тебе привет!', parse_mode='html')
    elif message.text.lower() == 'id':
        bot.send_message(message.chat.id, f'Твой ID: {message.from_user.id}', parse_mode='html')
    elif message.text.lower() == 'info':
        bot.send_message(message.chat.id, message, parse_mode='html')
    elif message.text.lower() == 'котик':
        bot.send_photo(message.chat.id, parser_pic(URL_PIC))
    elif message.text.lower() == 'шутка':
        bot.send_message(message.chat.id, list_of_jokes[0])
        del list_of_jokes[0]
    else:
        chat(message)


bot.polling(non_stop=True)