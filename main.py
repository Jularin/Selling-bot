# -*- coding: utf-8 -*-

import os
import telebot
import work_with_db
from datetime import datetime

bot = telebot.TeleBot('1088060110:AAF-s9TPSbMAhpOXFVUPj50S0Ya8hh38jAc')
types = telebot.types


# TO DO!! make funcs:main menu, add categories for items(2 or 3) add multiple buying


def logging(message):
    """Logging: write all commands in txt file"""
    info = "{}  Name: {} {} User id: {} message text: {}".format(str(datetime.now().strftime("%d-%m-%Y %H:%M")),
                                                                 str(message.from_user.first_name),
                                                                 str(message.from_user.last_name),
                                                                 str(message.chat.id),
                                                                 message.text)

    print("Username: " + str(message.from_user.username) + ", Name: " + str(message.from_user.first_name) + " " + str(
        message.from_user.last_name))
    print("User id: " + str(message.chat.id))
    with open('logs.txt', 'a', encoding='utf-8') as logs:
        logs.write(info + '\n')


def select_category(message):
    pass


@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    bot.answer_callback_query(callback_query_id=call.id, text='text')  # то что выведет при нажатии на кнопку
    if call.data == 'check_balance':
        bot.send_message(call.message.chat.id, 'BuTTON')
        bot.register_next_step_handler(call.message.chat.id, check_balance(call))


def advanced_keyboard(flag):
    markup = types.InlineKeyboardMarkup()  # create markup where put buttons
    if flag == 'user':
        check_balance_button = types.InlineKeyboardButton(text='Check Balance', callback_data='check_balance')
        markup.add(check_balance_button)

    return markup


@bot.message_handler(commands=['test'])
def test(message):
    bot.send_message(message.chat.id, "heyyy", reply_markup=advanced_keyboard('user'))


def keyboard(flag):
    """Function which generate keyboard."""
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)

    if flag == 'user':
        buy_button = types.KeyboardButton(text='/buy Купить товар')
        check_balance_button = types.KeyboardButton(text='/balance Баланс')
        help_button = types.KeyboardButton(text='/help  Помощь')
        keyboard.add(buy_button, check_balance_button, help_button)
        keyboard.add(types.KeyboardButton('/menu Главное меню'))

    elif flag == 'admin':
        dump_button = types.KeyboardButton(text='/dump нажмите сюда, чтобы получить дамп бд')
        change_balance_button = types.KeyboardButton(text='/changebalance нажмите сюда, чтобы получить дамп бд')
        add_user_button = types.KeyboardButton(text='/adduser нажмите сюда, чтобы получить дамп бд')
        mailing_button = types.KeyboardButton(text='/mailing нажмите сюда, чтобы получить дамп бд')
        logs_button = types.KeyboardButton(text='/logs txt файл логов')
        clear_logs_button = types.KeyboardButton(text='/clearlogs очистка файла логов')
        keyboard.add(dump_button, change_balance_button, add_user_button, mailing_button, logs_button, clear_logs_button)

    return keyboard


@bot.message_handler(commands=['menu'])
def main_menu(message):  # does't finished yet
    logging(message)


@bot.message_handler(commands=['start'])
def start(message):
    """Start function"""
    logging(message)
    work_with_db.check_in_db(message)
    bot.send_message(message.chat.id,
                     "You're using new bot! 'DESCRIPTION'\n/dump\n/balance\n/adduser\n/changebalance\n/adduser\n/help",
                     # here description of bot
                     reply_markup=keyboard('user'))


@bot.message_handler(commands=['help'])
def help_command(message):
    logging(message)
    bot.send_message(message.chat.id, 'Coded by M K (@topkekl)', reply_markup=keyboard('user'))


@bot.message_handler(commands=['buy'])
def buy_bot(message):
    """Buying items"""
    logging(message)
    try:
        with open('items.txt', encoding='utf-8') as items:
            if len(items.readlines()) > 0:
                if float(work_with_db.find_and_return_value(str(message.chat.id), 2)) >= 10:
                    work_with_db.change_balance(message.chat.id, -10)
                    with open('items.txt', encoding='utf-8') as inp:
                        item = inp.readline()
                        bot.send_message(message.chat.id, item, reply_markup=keyboard('user'))
                        lines = inp.readlines()
                    with open('items.txt', 'w', encoding='utf-8') as out:
                        out.writelines(lines)
                else:
                    bot.send_message(message.chat.id, "У вас не хватает денег", reply_markup=keyboard('user'))

            else:
                bot.send_message(message.chat.id, 'Товара нет в наличии', reply_markup=keyboard('user'))
                keyboard(0)
    except Exception as e:
        print(e)


@bot.message_handler(commands=['balance'])
def check_balance(message):
    """Send balance to user"""
    logging(message)
    work_with_db.check_in_db(message)
    bot.send_message(message.chat.id,
                     "Your balance: {} RUB".format(work_with_db.find_and_return_value(str(message.chat.id), 2)),
                     reply_markup=keyboard('user'))


@bot.message_handler(commands=['admin'])
def admin(message):
    """Access to admin panel"""
    logging(message)
    if work_with_db.find_and_return_value(str(message.chat.id), 3) == 'admin':
        bot.send_message(message.chat.id, "Ok, you're admin!", reply_markup=keyboard('admin'))
    else:
        bot.send_message(message.chat.id, "You're not admin", reply_markup=keyboard('user'))


@bot.message_handler(commands=['clearlogs'])
def clear_logs(message):
    """Function clear logs"""
    send_logs(message)  # sending logs before clearing
    if work_with_db.find_and_return_value(str(message.chat.id), 3) == 'admin':
        with open('logs.txt', 'w'):  # clearing logs
            pass


@bot.message_handler(commands=['logs'])
def send_logs(message):
    logging(message)
    if work_with_db.find_and_return_value(str(message.chat.id), 3) == 'admin':
        with open('logs.txt', encoding='utf-8') as logs:
            bot.send_document(message.chat.id, logs)


@bot.message_handler(commands=['dump'])
def dump(message):
    """Send dump of db for admin"""
    logging(message)
    work_with_db.check_in_db(message)
    if work_with_db.find_and_return_value(str(message.chat.id), 3) == 'admin':  # if command called by admin
        database = work_with_db.dump()
        result = ""
        for tuple in database:
            result = result + " | ".join(map(str, tuple)) + "\n"
        bot.send_message(message.chat.id, result, reply_markup=keyboard('admin'))


def add_user(message):
    """Next step for add_user_bot function"""
    logging(message)
    bot.send_message(message.chat.id, work_with_db.add_user(str(message.text)), reply_markup=keyboard('admin'))


@bot.message_handler(commands=['adduser'])
def add_user_bot(message):
    """Add new user by admin"""
    logging(message)
    i = "FUCK FUCK FUCK"
    if work_with_db.find_and_return_value(str(message.chat.id), 3) == 'admin':  # if command called by admin
        bot.register_next_step_handler(bot.send_message(message.chat.id, "Укажите айди"), add_user)


def change_balance(message):
    """Change balance by admin"""
    logging(message)
    print(message.text)
    try:
        id, amount = message.text.split()
        if work_with_db.find_and_return_value(id, 0):
            amount = int(amount)
            work_with_db.change_balance(id, amount)
            bot.send_message(message.chat.id,
                             "Баланс изменён теперь он у: {}  = {} RUB".format(
                                 work_with_db.find_and_return_value(id, 1),
                                 work_with_db.find_and_return_value(id, 2)),
                             reply_markup=keyboard('admin'))
        else:
            bot.send_message(message.chat.id, "Такого пользователя не существует", reply_markup=keyboard('admin'))
    except Exception as e:
        print(e)


@bot.message_handler(command=['additems'])
def add_items(message):
    logging(message)
    bot.register_next_step_handler(message.chat.id, )


@bot.message_handler(commands=['changebalance'])
def change_balance_bot(message):
    """Check who want change balance and get id and amount for change"""
    logging(message)
    if work_with_db.find_and_return_value(str(message.chat.id), 3) == 'admin':  # if command called by admin
        bot.register_next_step_handler(
            bot.send_message(message.chat.id, "Укажите какой айди и на какую сумму изменить (через пробел)"),
            change_balance)


@bot.message_handler(commands=['drop'])
def drop_table(message):
    """Drop table by admin"""
    logging(message)
    work_with_db.check_in_db(message)
    if work_with_db.find_and_return_value(str(message.chat.id), 3) == 'admin':  # if command called by admin
        if work_with_db.find_and_return_value(str(message.chat.id), 3) == 'admin':
            bot.send_message(message.chat.id, work_with_db.drop_table(), reply_markup=keyboard('user'))


def mailing(message):
    """Mailing by users in database"""
    logging(message)
    database = work_with_db.dump()
    for tuples in database:
        try:
            bot.send_message(tuples[0], message.text)
        except Exception as e:
            print(e)
            print(work_with_db.delete_user(tuples[0]))
    bot.send_message(message.chat.id, "Mailing finished", reply_markup=keyboard('admin'))


@bot.message_handler(commands=['mailing'])
def mailing_bot(message):
    """Function get mailing text"""
    logging(message)
    if work_with_db.find_and_return_value(str(message.chat.id), 3) == 'admin':  # if command called by admin
        bot.register_next_step_handler(bot.send_message(message.chat.id, "Send me text to mailing"), mailing)


# ADD NEW COMMANDS ONLY ABOVE THIS FUNC. New commands don't read bc all will be 'content_types = text'
@bot.message_handler(content_types=['text'])
def handle_message_received(message):
    logging(message)
    print(message.text)
    work_with_db.check_in_db(message)


bot.polling()
