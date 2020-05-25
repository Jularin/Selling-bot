# -*- coding: utf-8 -*-

import telebot
import work_with_db

bot = telebot.TeleBot('1088060110:AAF-s9TPSbMAhpOXFVUPj50S0Ya8hh38jAc')


@bot.message_handler(commands=['start'])
def start(message):
    work_with_db.check_in_db(message)
    bot.send_message(message.chat.id,
                     "You're using new bot! 'DESCRIPTION'\n/dump\n/balance\n/adduser\n/changebalance\n/adduser")


@bot.message_handler(commands=['balance'])
def check_balance(message):
    work_with_db.check_in_db(message)
    bot.send_message(message.chat.id,
                     "Your balance: {} RUB".format(work_with_db.find_and_return_value(str(message.chat.id), 2)))


@bot.message_handler(commands=['dump'])
def dump(message):
    work_with_db.check_in_db(message)
    if work_with_db.find_and_return_value(str(message.chat.id), 3) == 'admin':  # if command called by admin
        database = work_with_db.dump()
        result = ""
        for tuple in database:
            result = result + " | ".join(map(str, tuple)) + "\n"
        bot.send_message(message.chat.id, result)


def add_user(message):
    bot.send_message(message.chat.id, work_with_db.add_user(str(message.text)))


@bot.message_handler(commands=['adduser'])
def add_user_bot(message):
    bot.register_next_step_handler(bot.send_message(message.chat.id, "Укажите айди"), add_user)


def change_balance(message):
    print(message.text)
    id, amount = message.text.split()
    amount = int(amount)
    bot.send_message(message.chat.id, work_with_db.change_balance(id, amount))


@bot.message_handler(commands=['changebalance'])
def change_balance_bot(message):
    bot.register_next_step_handler(
        bot.send_message(message.chat.id, "Укажите какой айди и на какую сумму изменить (через пробел)"),
        change_balance)


@bot.message_handler(commands=['drop'])
def drop_table(message):
    work_with_db.check_in_db(message)
    if work_with_db.find_and_return_value(str(message.chat.id), 3) == 'admin':
        bot.send_message(message.chat.id, work_with_db.drop_table())


@bot.message_handler(commands=['sendmessage'])
def send_message(message):
    bot.register_next_step_handler(bot.send_message(message.chat.id, "Send me id"), send_message)


def mailing(message):
    database = work_with_db.dump()
    for tuples in database:
        try:
            bot.send_message(tuples[0], message.text)
        except Exception as e:
            print(e)
            print(work_with_db.delete_user(tuples[0]))


@bot.message_handler(commands=['mailing'])
def mailing_bot(message):
    bot.register_next_step_handler(bot.send_message(message.chat.id, "Send me text to mailing"), mailing)


# ADD NEW COMMANDS ONLY ABOVE THIS FUNC. New commands don't read bc all will be 'content_types = text'
@bot.message_handler(content_types=['text'])
def handle_message_received(message):
    print(message.text)
    work_with_db.check_in_db(message)


bot.polling()
