import sqlite3


def find_and_return_value(id, index):  # searching by id and return value
    """ID index 0, USERNAME index 1, BALANCE index 2, ROLE index 3"""
    con = sqlite3.connect("main.db")  # создание подключения
    cur = con.cursor()  # создание оюъекта курсор
    database = cur.execute("SELECT * FROM users")  # database dump
    for row in database:
        if row[0] == id:
            cur.close()
            con.close()
            return row[index]
    return False


def finding_in_db(finding, database, index):
    for row in database:
        if row[index] == finding:
            return True
    return False


def check_in_db(message):
    id = str(message.chat.id)
    username = "@" + str(message.from_user.username)

    con = sqlite3.connect("main.db")  # создание подключения
    cur = con.cursor()  # создание оюъекта курсор
    users = cur.execute("SELECT * FROM users")  # database dump

    if finding_in_db(id, users, 0):  # поиск пользователя по айди
        if finding_in_db(username, users, 1):  # поиск пользователя по юзернейму
            print("Вы уже зарегистрированы!")
            cur.close()
            con.close()

        else:
            sql = 'UPDATE users SET username = "{}" WHERE id = "{}"'.format(username, id)
            try:
                cur.execute(sql)
                print("Юзернейм обновлен " + username)
                con.commit()
                cur.close()
                con.close()
            except Exception as e:
                print(e)

    else:
        sql = 'INSERT INTO users (id,username, balance, role) VALUES("{}", "{}", "0.0", "user")'.format(id, username)

        try:
            cur.execute(sql)
        except Exception as e:
            print(e)
        else:
            print("Новый пользователь - " + username)
            con.commit()
            cur.close()
            con.close()


def dump():
    con = sqlite3.connect("main.db")  # создание подключения
    cur = con.cursor()  # создание оюъекта курсор
    cur.execute("SELECT * FROM users")
    database = cur.fetchall()
    cur.close()
    con.close()
    return database


def drop_table():
    con = sqlite3.connect("main.db")  # создание подключения
    cur = con.cursor()  # создание оюъекта курсор
    try:
        cur.execute("DELETE FROM users")
    except Exception as e:
        return "Что-то пошло не так ошибка: \n" + str(e)
    else:
        con.commit()
        cur.close()
        con.close()
        return "База данных успешно удалена"


def change_balance(id, amount):
    con = sqlite3.connect("main.db")  # создание подключения
    cur = con.cursor()  # создание оюъекта курсор
    try:
        sql = 'UPDATE users SET balance = balance + "{}" WHERE id = "{}"'.format(amount, id)
        cur.execute(sql)
        con.commit()
        cur.close()
        con.close()

    except Exception as e:
        print(e)
        cur.close()
        con.close()


def add_user(id):
    con = sqlite3.connect("main.db")  # создание подключения
    cur = con.cursor()  # создание оюъекта курсор
    cur.execute("INSERT INTO users VALUES ('{}', '@', 0.0, 'user')".format(id))
    con.commit()
    cur.close()
    con.close()
    return "User with id: {} added".format(id)


def delete_user(user_id):
    con = sqlite3.connect("main.db")  # создание подключения
    cur = con.cursor()  # создание оюъекта курсор
    cur.execute("DELETE FROM users WHERE id = '{}'".format(user_id))
    con.commit()
    cur.close()
    con.close()
    return "User with id: {} deleted".format(user_id)


def add_invoice_id(user_id, invoice_id, datetime):
    con = sqlite3.connect("main.db")  # создание подключения
    cur = con.cursor()  # создание оюъекта курсор
    cur.execute("INSERT INTO payments (id, invoice_id, datetime) VALUES ('{}', '{}', '{}')".format(user_id, invoice_id, datetime))
    con.commit()
    cur.close()
    con.close()
    return "Successful"


def dump_payments():
    con = sqlite3.connect("main.db")  # создание подключения
    cur = con.cursor()  # создание оюъекта курсор
    database = list(cur.execute("SELECT * FROM payments"))
    con.commit()
    cur.close()
    con.close()
    return database


def payment(invoice_id, amount):
    try:
        con = sqlite3.connect("main.db")  # создание подключения
        cur = con.cursor()  # создание оюъекта курсор
        user_id = list((cur.execute("SELECT * FROM payments WHERE invoice_id ='{}'".format(invoice_id))))[0][0]
        cur.execute("DELETE FROM payments WHERE invoice_id = '{}'".format(invoice_id))
        cur.execute("INSERT INTO completed_payments (id, invoice_id) VALUES ('{}', '{}'".format(user_id, invoice_id))
        con.commit()
        cur.close()
        con.close()
        change_balance(user_id, amount)
        print("successful")

    except Exception as e:
        print(e)


def deleting_invoices(invoice_id):
    try:
        con = sqlite3.connect("main.db")  # создание подключения
        cur = con.cursor()  # создание оюъекта курсор
        cur.execute("DELETE FROM payments WHERE invoice_id = '{}'".format(invoice_id))
        con.commit()
        cur.close()
        con.close()
        print("successful")

    except Exception as e:
        print(e)

