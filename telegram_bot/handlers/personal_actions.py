from aiogram import types
from dispatcher import dp
from mini_api import Api
from config import white_users, APP_HOST


@dp.message_handler(commands=['start'])
async def send_welcome(msg: types.Message):
    try:
        if msg.from_user.id not in white_users.values():
            return await msg.reply("Пробач, але я не можу тобі відповісти.")
        api_response = await Api([k for k, v in white_users.items() if v == msg.from_user.id][0]).create_user()
        body = api_response["user"]
        await msg.answer(
            "Привіт, <i>%s</i>! Ось дані для авторизації:"
            "\nЛогін: <code>%s</code>\nПароль: <code>%s</code>\nТакож ось адреса для авторизації: %s" % (
                msg.from_user.full_name, body["username"], body["password"], APP_HOST
            )
        )
    except Exception as e:
        await msg.answer("Виникла помилка під час виконання операції.\nВиключення: <code>%s</code>" %
                         e.__class__.__name__)
