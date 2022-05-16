from django.conf import settings
import asyncio
# from .LockAccount import LockingAccount
from aiogram import Bot, Dispatcher, types, executor

# Инициализация бота
token_telegram = settings.TELEGRAM_TOKEN
bot = Bot(token=token_telegram)
loop = asyncio.get_event_loop()
dp = Dispatcher(bot=bot, loop=loop)

# Подключение к СУБД
print("telega.py started...")


# Функция срабатывающая при запуске бота
@dp.message_handler(commands=['start'])
async def start_message(message):
    print("start")
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item4 = types.KeyboardButton("Заблокировать аккаунт")
    markup.add(item4)
    await bot.send_message(message.chat.id, "Приятной работы", reply_markup=markup)


# Основной функционал бота
@dp.message_handler(content_types=['text'])
async def other(message):
    chat_id = message.chat.id
    cur = con.cursor()
    # Кнопка блокировки аккаунта
    if message.text == 'Заблокировать аккаунт':
        LockingAccount(chat_id)
        await bot.send_message(chat_id, "Ваш аккаунт заблокирован")

    elif len(message.text) > 1:
        cur.execute(f"SELECT * FROM users where id_user_messenger={chat_id};")
        usr = cur.fetchone()
        # Проверка кода
        if usr is None:  # Аккаунт не привязан к коду
            cur.execute(f"SELECT * FROM users where key_messenger=\'{message.text}\';")
            ky = (cur.fetchone())

            if ky is None:
                await bot.send_message(chat_id, "Неверный ключ")

            else:
                # if ky[6]==None: cur.execute(f"UPDATE users SET id_user_messenger=\'{chat_id}\' WHERE
                # key_messenger=\'{message.text}\';") bot.send_message(chat_id, "Вы успешно авторизовались")

                cur.execute(f"SELECT id_user_messenger FROM users where key_messenger=\'{message.text}\';")
                lzh_ky = (cur.fetchone()[0])

                if lzh_ky is not None:
                    await bot.send_message(chat_id, "Неверный ключ")
                else:
                    await bot.send_message(chat_id, "Вы успешно авторизовались в мессенджере")
                    cur.execute(
                        f"UPDATE users SET id_user_messenger=\'{chat_id}\' WHERE key_messenger=\'{message.text}\';")
        # Проверка на ежедневную авторизацию
        else:
            cur.execute(f"SELECT is_login_today FROM users where id_user_messenger={chat_id};")
            is_log_day = (cur.fetchone()[0])
            if not is_log_day:
                cur.execute(f"SELECT key_messenger FROM users where id_user_messenger={chat_id};")
                keycode = cur.fetchone()[0]
                if keycode == message.text:
                    cur.execute(f"UPDATE users SET is_login_today=true WHERE key_messenger='{message.text}';")
                    await bot.send_message(chat_id, "Вы успешно авторизовались на текущий день")
                else:
                    await bot.send_message(chat_id, "Неверный код")
            else:
                await bot.send_message(chat_id, "Вы уже авторизовались")

    con.commit()
    cur.close()


# Сброс ежеедневной авторизации
# async def scheduler():
#     aioschedule.every().day.at("00:00").do(ResetBool)
#     aioschedule.every().day.at("07:00").do(MessageAllUsers)
#     while True:
#         await aioschedule.run_pending()
#         await asyncio.sleep(1)


# Сброс будет происходить параллельно от общего функционала
# async def on_startup(dp):
#     asyncio.create_task(scheduler())


def start():
    executor.start_polling(dispatcher=dp)
