import config
import asyncio

con=config.con

async def ResetBool():
    cur = con.cursor()
    cur.execute(f"SELECT * FROM users;")

    for i in cur.fetchall():
        cur.execute(f"UPDATE users SET is_login_today=false WHERE id='{i[0]}';")
    cur.close()
    con.commit()
