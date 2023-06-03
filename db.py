import sqlite3 as sq

db = sq.connect('main.db')
cur = db.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    balance INTEGER 
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS curency (
    id INTEGER PRIMARY KEY,
    rub TEXT ,
    uah TEXT 
)
""")


async def create_profile(user_id,  balance=0,):
    print('i here', user_id)
    user = cur.execute("SELECT * FROM users WHERE user_id == '{key}'".format(key=user_id)).fetchall()
    if not user:
        print('Create new user...')
        cur.execute("INSERT INTO 'users' ('user_id', 'balance') VALUES(?,?)", (user_id, balance))
        db.commit()


async def change_rubb(text):
    print('test')
    cur.execute(f"UPDATE curency SET rub = {text}")
    db.commit()


async def change_uah(text):
    cur.execute(f"UPDATE curency SET uah = {text}")
    db.commit()

async def get_rub():
    x = cur.execute(f"SELECT rub FROM curency").fetchall()[0][0]
    return x

async def get_ua():
    x = cur.execute(f"SELECT uah FROM curency").fetchall()[0][0]
    return x
