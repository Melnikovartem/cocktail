import telebot
import random
from telebot import types
from db import next_question, new_user, lazy, all_users
from threading import Thread
from time import sleep
from random import shuffle

telebot.apihelper.proxy = {'https': 'socks5h://geek:socks@t.geekclass.ru:7777'}
token = "969755030:AAH8X0ouUxKZeumKoczlXJG0PFaxzsUR-vQ"
bot = telebot.TeleBot(token=token)
stickers = ['\xF0\x9F\x98\xB1', '\xF0\x9F\x98\xA1', '\xF0\x9F\x98\x8E', '\xF0\x9F\x92\xA9', '\xF0\x9F\x92\xAA', '\xF0\x9F\x98\x98']

@bot.message_handler(commands=['help'])
def help_message(message):
    bot.send_message(message.chat.id, '/help :\n')

@bot.message_handler(commands=['start'])
def start_message(message):
    help_message(message)
    name=message.chat.first_name+" "+message.chat.last_name
    if(message.chat.username!=0): us=message.chat.username
    else: us="-"
    new_user(message.chat.id,name,us)
    questions_start(message)

def question_ask(user_id,question): #Получает ID и вопрос. создает клаву и выводит вопрос
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    list_items = stickers
    shuffle(list_items)
    for item in list_items:
        markup.add(item)
    bot.send_message(user_id, question,reply_markup=markup)

@bot.message_handler(content_types=['text'])
def send_text(message):
    res=next_question(message.chat.id,str(stickers.index(message.text)+1))
    if(res==-2):
        bot.send_message(message.chat.id,"Вопрос уже снят с рассмотрения")
    if(res==-1):
        bot.send_message(message.chat.id,"Спасибо за ваш отзыв")
    else:
        question_ask(message.chat.id,res)

bot.polling()
