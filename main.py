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

    print(info)

    with open('logs.txt', 'a', encoding='utf-8') as logs:
        logs.write(info + '\n')


def call_logging(call):
    """Logging callbacks"""
    info = '{} User ID: {} callback: {} '.format(str(datetime.now().strftime("%d-%m-%Y %H:%M")),
                                                 str(call.message.chat.id),
                                                 str(call.data))
    print(info)

    with open("logs.txt", 'a', encoding='utf-8') as logs:
        logs.write(info + '\n')


def check_and_send_categories(call):
    result = []
    categories = os.listdir('items')  # list of names in folder with products
    os.chdir('items')
    for category in categories:
        with open(category, 'r') as product:
            result.append([category[:-4], str(len(product.readlines()))])
    os.chdir('..')  # up to one level of paths
    result1 = []
    for values in result:
        result1.append(" ".join(values))
    bot.send_message(call.message.chat.id, " | ".join(result1))  # send message ex: ebay 96 | eu 84 | usa 30


'''
@bot.callback_query_handler(func=lambda call: True)
def category_query_handler(call):
    array = select_category()
    for callback in array:
        if call.data == callback+'_buy':
            buy_bot(callback+'.txt')
        elif call.data == callback+'_add':
            bot.register_next_step_handler(bot.send_message(call.message.chat.id, "Send me txt file to add"), add_items)


def make_keyboard_from_list(array):
    markup = types.InlineKeyboardMarkup()
    for button in array:
        markup.add(types.InlineKeyboardButton(text=str(button), callback_data=str(button)+'_buy'))

    return markup


def select_category():
    result = []
    categories = os.listdir('items')
    for category in categories:
        result.append(category[:-4])

    return result
'''


@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    bot.answer_callback_query(callback_query_id=call.id,
                              text='You clicked to button!')  # то что выведет при нажатии на кнопку
    call_logging(call)
    if call.data == 'check_balance':
        check_balance(call)
    elif call.data == 'add_user':
        add_user_bot(call)
    elif call.data == 'dump':
        dump(call)
    elif call.data == 'mailing':
        mailing_bot(call)
    elif call.data == 'change_balance':
        change_balance_bot(call)
    elif call.data == 'send_logs':
        send_logs(call)
    elif call.data == 'clear_logs':
        clear_logs(call)
    elif call.data == 'buy':
        buy_bot(call)
    elif call.data == 'help':
        help_command(call)
    elif call.data == 'menu':
        main_menu(call)
    elif call.data == 'categories':
        check_and_send_categories(call)
    elif call.data == 'add_items':
        add_items(call)


def advanced_keyboard(flag):
    markup = types.InlineKeyboardMarkup()  # create markup where put buttons

    if flag == 'user':
        check_balance_button = types.InlineKeyboardButton(text='Check Balance', callback_data='check_balance')
        buy_button = types.InlineKeyboardButton(text='Buy', callback_data='buy')
        help_button = types.InlineKeyboardButton(text="Help", callback_data='help')
        menu_button = types.InlineKeyboardButton(text="Menu", callback_data='menu')
        check_categories_button = types.InlineKeyboardButton(text="Categories and counts", callback_data='categories')
        markup.add(check_balance_button, buy_button, help_button, menu_button, check_categories_button)

    if flag == 'admin':
        add_user_button = types.InlineKeyboardButton(text="Add user", callback_data='add_user')
        dump_button = types.InlineKeyboardButton(text='Dump Database', callback_data='dump')
        mailing_button = types.InlineKeyboardButton(text='Mailing', callback_data='mailing')
        change_balance_button = types.InlineKeyboardButton(text='Change balance', callback_data='change_balance')
        logs_button = types.InlineKeyboardButton(text='Send logs', callback_data='send_logs')
        clear_logs_button = types.InlineKeyboardButton(text='Clear logs', callback_data='clear_logs')
        add_items_button = types.InlineKeyboardButton(text='Add items', callback_data='add_items')
        markup.add(add_user_button, dump_button, mailing_button, change_balance_button, logs_button, clear_logs_button, add_items_button)

    return markup


def main_menu(call):  # does't finished yet
    bot.send_message(call.message.chat.id,
                     "You're using new bot! 'DESCRIPTION'",
                     reply_markup=advanced_keyboard('user'))  # here description of bot


@bot.message_handler(commands=['start'])
def start(message):
    """Start function"""
    logging(message)
    work_with_db.check_in_db(message)
    bot.send_message(message.chat.id,
                     "You're using new bot! 'DESCRIPTION'",
                     # here description of bot
                     reply_markup=advanced_keyboard('user'))


def help_command(call):
    bot.send_message(call.message.chat.id, 'Coded by M K (@topkekl)')


def buying(call, category, count):
    pass


def buy_bot(call):
    """Buying items"""
    try:
        with open('items.txt', encoding='utf-8') as items:
            if len(items.readlines()) > 0:
                if float(work_with_db.find_and_return_value(str(call.message.chat.id), 2)) >= 10:
                    work_with_db.change_balance(call.message.chat.id, -10)
                    with open('items.txt', encoding='utf-8') as inp:
                        item = inp.readline()
                        bot.send_message(call.message.chat.id, item)
                        lines = inp.readlines()
                    with open('items.txt', 'w', encoding='utf-8') as out:
                        out.writelines(lines)
                else:
                    bot.send_message(call.message.chat.id, "У вас не хватает денег")

            else:
                bot.send_message(call.message.chat.id, 'Товара нет в наличии')
    except Exception as e:
        print(e)


def check_balance(call):
    """Send balance to user"""
    bot.send_message(call.message.chat.id,
                     "Your balance: {} RUB".format(work_with_db.find_and_return_value(str(call.message.chat.id), 2)))


@bot.message_handler(commands=['admin'])
def admin(message):
    """Access to admin panel"""
    logging(message)
    if work_with_db.find_and_return_value(str(message.chat.id), 3) == 'admin':
        bot.send_message(message.chat.id, "Ok, you're admin!", reply_markup=advanced_keyboard('admin'))
    else:
        bot.send_message(message.chat.id, "You're not admin")


def clear_logs(call):
    """Function clear logs"""
    send_logs(call)  # sending logs before clearing
    if work_with_db.find_and_return_value(str(call.message.chat.id), 3) == 'admin':
        with open('logs.txt', 'w'):  # clearing logs
            pass


def send_logs(call):
    if work_with_db.find_and_return_value(str(call.message.chat.id), 3) == 'admin':
        with open('logs.txt', encoding='utf-8') as logs:
            bot.send_document(call.message.chat.id, logs)


def dump(call):
    """Send dump of db for admin"""
    # work_with_db.check_in_db(message)
    if work_with_db.find_and_return_value(str(call.message.chat.id), 3) == 'admin':  # if command called by admin
        database = work_with_db.dump()
        result = ""
        for row in database:
            result = result + " | ".join(map(str, row)) + "\n"
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='KEKW', reply_markup=advanced_keyboard('admin'))
        bot.send_message(call.message.chat.id, result)


def add_user(message):
    """Next step for add_user_bot function"""
    logging(message)
    bot.send_message(message.chat.id, work_with_db.add_user(str(message.text)))


def add_user_bot(call):
    """Add new user by admin"""
    if work_with_db.find_and_return_value(str(call.message.chat.id), 3) == 'admin':  # if command called by admin
        bot.register_next_step_handler(bot.send_message(call.message.chat.id, "Укажите айди"), add_user)


def change_balance(message):
    """Change balance by admin"""
    logging(message)
    print(message.text)
    try:
        add_id, amount = message.text.split()
        if work_with_db.find_and_return_value(add_id, 0):
            amount = int(amount)
            work_with_db.change_balance(add_id, amount)
            bot.send_message(message.chat.id,
                             "Баланс изменён теперь он у: {}  = {} RUB".format(
                                 work_with_db.find_and_return_value(add_id, 1),
                                 work_with_db.find_and_return_value(add_id, 2)),
                             reply_markup=advanced_keyboard('admin'))
        else:
            bot.send_message(message.chat.id, "Такого пользователя не существует")
    except Exception as e:
        print(e)


def add_items(call):
    bot.send_message(call.message.chat.id, "OK I'm here")


def change_balance_bot(call):
    """Check who want change balance and get id and amount for change"""
    if work_with_db.find_and_return_value(str(call.message.chat.id), 3) == 'admin':  # if command called by admin
        bot.register_next_step_handler(
            bot.send_message(call.message.chat.id, "Укажите какой айди и на какую сумму изменить (через пробел)"),
            change_balance)


@bot.message_handler(commands=['drop'])
def drop_table(message):
    """Drop table by admin"""
    logging(message)
    work_with_db.check_in_db(message)
    if work_with_db.find_and_return_value(str(message.chat.id), 3) == 'admin':  # if command called by admin
        if work_with_db.find_and_return_value(str(message.chat.id), 3) == 'admin':
            bot.send_message(message.chat.id, work_with_db.drop_table(), reply_markup=advanced_keyboard('user'))


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
    bot.send_message(message.chat.id, "Mailing finished")


def mailing_bot(call):
    """Function get mailing text"""

    if work_with_db.find_and_return_value(str(call.message.chat.id), 3) == 'admin':  # if command called by admin
        bot.register_next_step_handler(bot.send_message(call.message.chat.id, "Send me text to mailing"), mailing)


# ADD NEW COMMANDS ONLY ABOVE THIS FUNC. New commands don't read bc all will be 'content_types = text'
@bot.message_handler(content_types=['text'])
def handle_message_received(message):
    logging(message)
    print(message.text)
    work_with_db.check_in_db(message)


bot.polling()
