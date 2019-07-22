import telebot
import random
from telebot import types
from db import next_question, new_user, lazy, all_users
from threading import Thread
from time import sleep

telebot.apihelper.proxy = {'https': 'socks5h://geek:socks@t.geekclass.ru:7777'}
token = "704179718:AAEGoZT__GbVcAEhYW93ww_XNUto8V0RThA"
bot = telebot.TeleBot(token=token)
stickers = []

@bot.message_handler(commands=['help'])
def help_message(message):
    bot.send_message(message.chat.id,'В течение смены GoTo данный бот отправляет вам несколько вопросов. По этим вопросам составляется статистика. /stats предоставляет статистику о ваших ответах')
@bot.message_handler(commands=['stats'])
def stats_message(message):
    bot.send_message(message.chat.id,'Скоро в программе')
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет, ты написал нам /start. Спасибо, что присоединился к нам. Жди новых опросов. Напишите /help для справки')
    name=message.chat.first_name+message.chat.last_name
    if(message.chat.username!=0): us=message.chat.username
    else: us="-"
    new_user(message.chat.id,name,us)

def questions_start(user_id):
    q=next_question(user_id, "")
    question_ask(user_id,q)

def question_ask(user_id,question): #Получает ID и вопрос. создает клаву и выводит вопрос
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup.row('1','2','3')
    markup.row('4','5','6')
    markup.row('7','8','9')
    bot.send_message(user_id, question,reply_markup=markup)

@bot.message_handler(content_types=['text'])
def send_text(message):
    #res=next_question(message.chat.id,int(message.text))
    res='3*3'
    if(res==-2):
        bot.send_message(message.chat.id,"Вопрос уже снят с рассмотрения")
    if(res==-1):
        bot.send_message(message.chat.id,"Спасибо за ваш отзыв")
    else:
        question_ask(message.chat.id,res)
def notification(user_id):
    bot.send_message(user_id,"Не забудьте ответить на наши вопросы")
    res=next_question(message.chat.id,0)


def f():
    a=0
    n=0
    while True:
        print("-",n)
        if(n%12==1):
            for i in all_users():
                questions_start(i)
        if(n%12==2):
            for i in lazy(): notification(i)
        if(n%12==4):
            for i in lazy(): bot.send_message(i,"ОПРОС ЗАКРЫТ")
        n+=1
        sleep(40)

Thread(target=f).start()
bot.polling()
