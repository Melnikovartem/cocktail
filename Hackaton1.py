import telebot
import random
from telebot import types
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
Tele_users=[]#массив ID пользователей
question_last={}#словарь ID->последний заданный вопрос
reading_mode={}#0 - ввести имя. 1 - ответ на вопрос
telebot.apihelper.proxy = {'https': 'socks5h://geek:socks@t.geekclass.ru:7777'}
token = "704179718:AAEGoZT__GbVcAEhYW93ww_XNUto8V0RThA"
bot = telebot.TeleBot(token=token)
stickers = []
@bot.message_handler(commands=['start'])
def start_message(message):#запомнит ID. Поставит reading_mode=0
    bot.send_message(message.chat.id, 'Привет, ты написал нам /start. Спасибо, что присоединился к нам. Напиши нам свое имя.')
    reading_mode=0
    Tele_users.append([message.chat.id])
def questions_start(user_id):
    q=start_poll(user_id)
    question_ask(user_id,q)
def question_ask(user_id,question): #Получает ID и вопрос. создает клаву и выводит вопрос
    global questions_last
    questions_last[user_id]=question
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup.row(question[1],question[2],question[3])
    markup.row(question[4],question[5],question[6])
    markup.row(question[7],question[8],question[9])
    reading_mode[user_id]=1
    for i in Tele_isers:
        bot.send_message(user_id, question[0],reply_markup=markup)
@bot.message_handler(content_types=['text'])
def send_text(message):
    if(reading_mode[message.chat.id]==0):
        print()
       
        new_user(message.chat.id,message.text)
        reading_mode[message.chat.id]=100
    if(reading_mode[message.chat.id]==1):
        res=next_question(message.chat.id,int(message.text))
        if(res==-2):
            bot.send_message(message.chat.id, "Вы дали некоректный ответ. вам придется ответить на вопрос заново.")
            quetion_ask(qestion_last)
        elif(res==-1):
            bot.send_message(message.chat.id,"Спасибо за ваш отзыв")
        else:
            question_ask(massage.chat.id,question)
def notification(user_id):
    bot.send_message(message.chat.id,"Не забудьте ответить на наши вопросы")
    question_ask(user_id,question_last[user_id])
bot.polling()
