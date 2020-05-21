# -*- coding: utf-8 -*-

import sqlite3

def finding_in_db(finding, database, index):
    for row in database:
        if row[index] == finding:
            return True
    return False

for _ in range(int(input("Сколько пользователей обработать? "))):
    id, username = input("Введите айди и юзернейм").split()

    con = sqlite3.connect("users.db") #создание подключения
    cur = con.cursor() #создание оюъекта курсор
    users = cur.execute("SELECT * FROM users")

    if finding_in_db(id, users, 0): #поиск пользователя по айди
        if finding_in_db(username, users, 1): # поиск пользователя по юзернейму
            print("Вы уже зарегистрированы!")
        else:
            sql = 'UPDATE users SET username = "{}" WHERE id = "{}"'.format(username, id)
            try:
                cur.execute(sql)
            except Exception as e:
                print(e)
            else:
                print("Ваш юзернейм обновлёг!")
                con.commit()
    else:
        sql = 'INSERT INTO users (id,username, balance, role) VALUES("{}", "{}", "0.0", "user")'.format(id, username)

        try:
            cur.execute(sql)
        except Exception as e:
            print(e)
        else:
            print("Вы успешно зарегистрировались!")
            con.commit()

    cur.execute("SELECT * FROM users") #вывод таблицы
    print(cur.fetchall())
    cur.close()
    con.close()
input()
