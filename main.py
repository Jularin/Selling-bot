# -*- coding: utf-8 -*-

import telebot
import sqlite3
import work_with_db

bot = telebot.TeleBot('1088060110:AAF-s9TPSbMAhpOXFVUPj50S0Ya8hh38jAc')


@bot.message_handler(commands=['start'])
def start(message):
    work_with_db.check_in_db(message)
    bot.send_message(message.chat.id, "You're using new bot! 'DESCRIPTION'\n/dump\n/balance\n")


@bot.message_handler(commands=['balance'])
def check_balance(message):
    work_with_db.check_in_db(message)
    bot.send_message(message.chat.id, "Your balance: {} RUB".format(work_with_db.find_and_return_value(str(message.chat.id), 2)))


@bot.message_handler(commands=['dump'])
def dump(message):
    work_with_db.check_in_db(message)
    if work_with_db.find_and_return_value(str(message.chat.id), 3) == 'admin':
        database = work_with_db.dump()
        result = ""
        for tuple in database:
                result = result + " | ".join(map(str, tuple)) + "\n"
        bot.send_message(message.chat.id, result)


@bot.message_handler(commands=['drop'])
def drop_table(message):
    work_with_db.check_in_db(message)
    if work_with_db.find_and_return_value(str(message.chat.id), 3) == 'admin':
        bot.send_message(message.chat.id, work_with_db.drop_table())


@bot.message_handler(commands=['change_balance'])
def change_balance(message):
    bot.register_next_step_handler(bot.send_message(message.chat.id, "Укажите какой айди и на какую сумму изменить (через пробел)"), change_balance)


def change_balance(message):
    print(message.text)
    id, amount = (message.text).split()
    amount = int(amount)
    bot.send_message(message.chat.id, work_with_db.change_balance(id, amount))


@bot.message_handler(content_types=['text'])
def handle_message_received(message):
    pass


bot.polling()
