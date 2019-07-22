import telebot
import random
from telebot import types
from db import next_question

telebot.apihelper.proxy = {'https': 'socks5h://geek:socks@t.geekclass.ru:7777'}
token = "704179718:AAEGoZT__GbVcAEhYW93ww_XNUto8V0RThA"
bot = telebot.TeleBot(token=token)
stickers = []


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет, ты написал нам /start. Спасибо, что присоединился к нам. Напиши нам свое имя.')

@bot.message_handler(commands=['question'])
def questions_start(message):
    q=next_question(message.chat.id, "")
    question_ask(message.chat.id,q)

def question_ask(user_id,question): #Получает ID и вопрос. создает клаву и выводит вопрос
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup.row('1','2','3')
    markup.row('4','5','6')
    markup.row('7','8','9')
    bot.send_message(user_id, question[0],reply_markup=markup)


@bot.message_handler(content_types=['text'])
def send_text(message):
    question=next_question(message.chat.id,message.text)
    if(question==-1):
        bot.send_message(message.chat.id,"Спасибо за ваш отзыв")
    else:
        question_ask(message.chat.id, question)


def notification(user_id):
    bot.send_message(message.chat.id,"Не забудьте ответить на наши вопросы")
    question_ask(user_id,question_last[user_id])

bot.polling()
