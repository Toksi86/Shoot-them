import sqlite3 as sq

with sq.connect('st.db') as con:
    cur = con.cursor()

    cur.execute('SELECT * FROM users ORDER BY score DESC')
    # result = cur.fetchall() # сохранить данные в переменную, удаляет из cur
    for note in cur:
        print(note)

con.close()

# UPDATE - обновление записи: UPDATE users SET score WHERE name LIKE 'name'
