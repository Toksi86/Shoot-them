import sqlite3 as sq

with sq.connect('st.db') as con:
    cur = con.cursor()

    cur.execute('DROP TABLE IF EXISTS users')  # - удалить таблицу
    cur.execute('''CREATE TABLE IF NOT EXISTS users (
        name TEXT NOT NULL DEFAULT Incognito,
        score INTEGER NOT NULL DEFAULT 0
        )''')
con.close()

# Команды SQL
# INSTERT  - добавление записи в SQL
# SELECT - выборка данных из таблицы
