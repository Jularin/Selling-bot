# -*- coding: utf-8 -*-

from paying import create_invoice
import os
import telebot
import work_with_db
from datetime import datetime

bot = telebot.TeleBot('1088060110:AAF-s9TPSbMAhpOXFVUPj50S0Ya8hh38jAc')
types = telebot.types
categories = ["USA", "EU", "Ebay"]


# TO DO!! make funcs:main menu, add categories for items(2 or 3) add multiple buying

def error_logging(error_name):
    error_log = "[!!!] {} Error name: {}".format(str(datetime.now().strftime("%d-%m-%Y %H:%M")),
                                                 error_name)
    with open("logs.txt", 'a') as logs:
        logs.write(error_log + '\n')


def logging(message):
    """Logging: write all commands in txt file"""
    log = "{}  Name: {} {} User id: {} message text: {}".format((datetime.now().strftime("%d-%m-%Y %H:%M")),
                                                                str(message.from_user.first_name),
                                                                str(message.from_user.last_name),
                                                                str(message.chat.id),
                                                                message.text)

    print(log)

    with open('logs.txt', 'a', encoding='utf-8') as logs:
        logs.write(log + '\n')


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


@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    global categories
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
        category_choice(call)
    elif call.data == 'help':
        help_command(call)
    elif call.data == 'menu':
        main_menu(call)
    elif call.data == 'categories':
        check_and_send_categories(call)
    elif call.data == 'add_items':
        add_items(call)
    elif call.data == 'replenish':
        replenish_bot(call)
    elif call.data == 'usa':
        buying(call, 'usa', 20)
    elif call.data == 'eu':
        buying(call, 'eu', 15)
    elif call.data == 'ebay':
        buying(call, 'ebay', 10)


def advanced_keyboard(flag):
    global categories
    markup = types.InlineKeyboardMarkup()  # create markup where put buttons

    if flag == 'user':
        check_balance_button = types.InlineKeyboardButton(text='Check Balance', callback_data='check_balance')
        buy_button = types.InlineKeyboardButton(text='Buy', callback_data='buy')
        help_button = types.InlineKeyboardButton(text="Help", callback_data='help')
        menu_button = types.InlineKeyboardButton(text="Menu", callback_data='menu')
        check_categories_button = types.InlineKeyboardButton(text="Categories and counts", callback_data='categories')
        replenish_button = types.InlineKeyboardButton(text="Replenish your balance", callback_data='replenish')
        markup.add(check_balance_button, buy_button, help_button, menu_button, check_categories_button,
                   replenish_button)

    elif flag == 'admin':
        add_user_button = types.InlineKeyboardButton(text="Add user", callback_data='add_user')
        dump_button = types.InlineKeyboardButton(text='Dump Database', callback_data='dump')
        mailing_button = types.InlineKeyboardButton(text='Mailing', callback_data='mailing')
        change_balance_button = types.InlineKeyboardButton(text='Change balance', callback_data='change_balance')
        logs_button = types.InlineKeyboardButton(text='Send logs', callback_data='send_logs')
        clear_logs_button = types.InlineKeyboardButton(text='Clear logs', callback_data='clear_logs')
        add_items_button = types.InlineKeyboardButton(text='Add items', callback_data='add_items')
        markup.add(add_user_button, dump_button, mailing_button, change_balance_button, logs_button, clear_logs_button,
                   add_items_button)

    elif flag == 'categories':
        for category in categories:
            markup.add(types.InlineKeyboardButton(text=category, callback_data=category.lower()))
        markup.add(types.InlineKeyboardButton(text="Назад", callback_data='menu'))
    return markup


def replenish(message):
    amount = message.text
    invoice = create_invoice(amount)
    bot.send_message(message.chat.id, "{} - ссылка для пополнения счёта. Оплатить нужно за 30 минут".format(invoice[0]))
    work_with_db.add_invoice_id(message.chat.id, invoice[1], str(datetime.now()))


def replenish_bot(call):  # пополнение счёта
    bot.register_next_step_handler(bot.send_message(call.message.chat.id, "Введите сумму для пополнения в долларах"),
                                   replenish)


def main_menu(call):  # does't finished yet
    bot.edit_message_text(chat_id=call.message.chat.id,
                          message_id=call.message.message_id,
                          text="You're using new bot! 'DESCRIPTION'",
                          reply_markup=advanced_keyboard('user'))  # here description of bot


def category_choice(call):
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Выберете категорию:',
                          reply_markup=advanced_keyboard('categories'))


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


def buying(call, category, price):
    """Buying items"""
    try:
        os.chdir('items')
        with open('{}.txt'.format(category), encoding='utf-8') as items:
            if len(items.readlines()) > 0:
                os.chdir('..')
                if float(work_with_db.find_and_return_value(str(call.message.chat.id), 2)) >= price:
                    work_with_db.change_balance(call.message.chat.id, -price)
                    os.chdir('items')
                    with open('{}.txt'.format(category), encoding='utf-8') as inp:
                        item = inp.readline()
                        bot.send_message(call.message.chat.id, item)
                        lines = inp.readlines()
                    with open('{}.txt', 'w', encoding='utf-8') as out:
                        out.writelines(lines)
                    os.chdir('..')
                else:
                    os.chdir('..')
                    bot.send_message(call.message.chat.id, "У вас не хватает денег")

            else:
                os.chdir('..')
                bot.send_message(call.message.chat.id, 'Товара нет в наличии')
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text="You're using new bot! 'DESCRIPTION'",
                              reply_markup=advanced_keyboard('user'))
    except Exception as e:
        os.chdir('..')
        print(e)
        error_logging(e)


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
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='KEKW',
                              reply_markup=advanced_keyboard('admin'))
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


try:
    bot.polling()
except Exception as e:
    error_logging(e)
