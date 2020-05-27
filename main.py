# -*- coding: utf-8 -*-

import telebot
import work_with_db
from datetime import datetime

bot = telebot.TeleBot('1088060110:AAF-s9TPSbMAhpOXFVUPj50S0Ya8hh38jAc')
types = telebot.types

# TO DO!! make funcs: admin keyboard and users keyboard, main menu, add categories for items(2 or 3) add multiple buying


# Finish this func
def sure(message):
    bot.send_message(message.chat.id, "Are you sure? y/n")


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


def keyboard(flag):
    """Function which generate keyboard"""
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    buy_button = types.KeyboardButton(text='/buy Купить товар')
    check_balance_button = types.KeyboardButton(text='/balance Баланс')
    help_button = types.KeyboardButton(text='/help  Помощь')
    keyboard.add(buy_button, check_balance_button, help_button)
    if flag:
        keyboard.add(types.KeyboardButton('/start Главное меню'))
    return keyboard


@bot.message_handler(commands=['start'])
def start(message):
    """Main menu"""
    logging(message)
    work_with_db.check_in_db(message)
    bot.send_message(message.chat.id,
                     "You're using new bot! 'DESCRIPTION'\n/dump\n/balance\n/adduser\n/changebalance\n/adduser\n/help",  # here description of bot
                     reply_markup=keyboard(0))


@bot.message_handler(commands=['help'])
def help_command(message):
    logging(message)
    bot.send_message(message.chat.id, 'Coded by M K (@topkekl)', reply_markup=keyboard(1))


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
                        bot.send_message(message.chat.id, item, reply_markup=keyboard(1))
                        lines = inp.readlines()
                    with open('items.txt', 'w', encoding='utf-8') as out:
                        out.writelines(lines)
                else:
                    bot.send_message(message.chat.id, "У вас не хватает денег", reply_markup=keyboard(1))

            else:
                bot.send_message(message.chat.id, 'Товара нет в наличии', reply_markup=keyboard(1))
                keyboard(0)
    except Exception as e:
        print(e)


@bot.message_handler(commands=['balance'])
def check_balance(message):
    """Send balance to user"""
    logging(message)
    work_with_db.check_in_db(message)
    bot.send_message(message.chat.id,
                     "Your balance: {} RUB".format(work_with_db.find_and_return_value(str(message.chat.id), 2)), reply_markup=keyboard(1))


@bot.message_handler(commands=['admin'])
def admin(message):
    """Admin panel"""
    logging(message)
    if work_with_db.find_and_return_value(str(message.chat.id), 3) == 'admin':
        keyboard = types.ReplyKeyboardMarkup(row_width=2)
        dump_button = types.KeyboardButton(text='/dump нажмите сюда, чтобы получить дамп бд')
        change_balance_button = types.KeyboardButton(text='/changebalance нажмите сюда, чтобы получить дамп бд')
        add_user_button = types.KeyboardButton(text='/adduser нажмите сюда, чтобы получить дамп бд')
        mailing_button = types.KeyboardButton(text='/mailing нажмите сюда, чтобы получить дамп бд')

        keyboard.add(dump_button, change_balance_button, add_user_button, mailing_button)
        bot.send_message(message.chat.id, "Ok, you're admin!", reply_markup=keyboard)

    else:
        bot.send_message(message.chat.id, "You're not admin")


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
        bot.send_message(message.chat.id, result)


def add_user(message):
    """Next step for add_user_bot function"""
    logging(message)
    bot.send_message(message.chat.id, work_with_db.add_user(str(message.text)))


@bot.message_handler(commands=['adduser'])
def add_user_bot(message):
    """Add new user by admin"""
    logging(message)
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
                             "Баланс изменён теперь он у: {}  = {} RUB".format(work_with_db.find_and_return_value(id, 1),
                                                                               work_with_db.find_and_return_value(id, 2)))
        else:
            bot.send_message(message.chat.id, "Такого пользователя не существует")
    except Exception as e:
        print(e)


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
            bot.send_message(message.chat.id, work_with_db.drop_table())


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
