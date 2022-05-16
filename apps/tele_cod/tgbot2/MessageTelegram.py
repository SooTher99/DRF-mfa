#import telebot
from aiogram import Bot, Dispatcher
import config
token_telegram = config.TOKEN
#bot = telebot.TeleBot(token_telegram)
bot = Bot(token=token_telegram)
dp = Dispatcher(bot=bot)


con=config.con

async def MessageTelegramBot(chat_id, message):
    await bot.send_message(chat_id, message)


async def MessageAllUsers():
    cur=con.cursor()
    cur.execute(f"SELECT id_user_messenger FROM users where is_login_today=false and id_user_messenger is not NULL;")
    a=cur.fetchall()
    chat_id=''
    for i in a:
        chat_id=i[0]
        await bot.send_message(chat_id, "Пожалуйста авторизуйтесь в мессенджере")

    
async def MessegeLock(login, message):
    cur = con.cursor()
    cur.execute(f"SELECT id_user_messenger FROM users WHERE login='{login}';")
    id_user = cur.fetchone()[0]
    await bot.send_message(id_user,message)



