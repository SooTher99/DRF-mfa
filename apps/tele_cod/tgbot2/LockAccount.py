import time
import datetime
import psycopg2
import config


con = config.con


def LockingAccount(chat_id):
    cur = con.cursor()
    cur.execute(f"UPDATE users SET lock_account=true where id_user_messenger='{chat_id}';")
    con.commit()



def UnlockingAccount(login):
    cur = con.cursor()
    cur.execute(f"UPDATE users SET lock_account=false where login='{login}';")
    con.commit()

def IsLockAccount(login):
    cur = con.cursor()
    cur.execute(f"select lock_account from users where login='{login}';")

    return (cur.fetchone()[0])


