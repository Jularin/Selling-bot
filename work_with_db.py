import sqlite3


def find_and_return_value(id, index): #searching by id and return value
    """ID index 0, USERNAME index 1, BALANCE index 2, ROLE index 3"""
    con = sqlite3.connect("users.db") #создание подключения
    cur = con.cursor() #создание оюъекта курсор
    database = cur.execute("SELECT * FROM users")  #datebase dump
    for row in database:
        if row[0] == id:
            cur.close()
            con.close()
            return row[index]


def finding_in_db(finding, database, index):
    for row in database:
        if row[index] == finding:
            return True
    return False


def check_in_db(message):
    id = str(message.chat.id)
    username = "@" + str(message.from_user.username)

    con = sqlite3.connect("users.db") #создание подключения
    cur = con.cursor() #создание оюъекта курсор
    users = cur.execute("SELECT * FROM users")  #datebase dump

    if finding_in_db(id, users, 0): #поиск пользователя по айди
        if finding_in_db(username, users, 1): # поиск пользователя по юзернейму
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
    con = sqlite3.connect("users.db") #создание подключения
    cur = con.cursor() #создание оюъекта курсор
    cur.execute("SELECT * FROM users")
    database = cur.fetchall()
    cur.close()
    con.close()
    return database


def drop_table():
    con = sqlite3.connect("users.db") #создание подключения
    cur = con.cursor() #создание оюъекта курсор
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
    username = find_and_return_value(id, 1)
    con = sqlite3.connect("users.db") #создание подключения
    cur = con.cursor() #создание оюъекта курсор
    try:
        sql = 'UPDATE users SET balance = balance + "{}" WHERE id = "{}"'.format(amount, id)
        cur.execute(sql)
        con.commit()
        cur.close()
        con.close()
        return "Баланс изменён теперь он у: {}  = {} RUB".format(username, find_and_return_value(id, 2))

    except Exceptio as e:
        print(e)
        cur.close()
        con.close()

#print(change_balance('124512512', -10))
