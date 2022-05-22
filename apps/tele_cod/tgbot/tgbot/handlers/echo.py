from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.utils.markdown import hcode

async def register_user(message: types.Message):
    chat_id = message.chat.id
    # Кнопка блокировки аккаунта
    if message.text == 'Заблокировать аккаунт':
        await message.answer("\nВаш аккаунт заблокирован")

    elif len(message.text) > 5:
        cur.execute(f"SELECT * FROM users where id_user_messenger={chat_id};")
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




async def bot_echo(message: types.Message):
    text = [
        "Echo without state.",
        "Message:",
        message.text
    ]

    await message.answer('\n'.join(text))


# async def bot_echo_all(message: types.Message, state: FSMContext):
#     state_name = await state.get_state()
#     text = [
#         f'Echo in state {hcode(state_name)}',
#         'Message:',
#         hcode(message.text)
#     ]
#     await message.answer('\n'.join(text))


def register_echo(dp: Dispatcher):
    dp.register_message_handler(bot_echo)
    # dp.register_message_handler(bot_echo_all, state="*", content_types=types.ContentTypes.ANY)
