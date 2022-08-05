from aiogram import types
from telegram_bot.dispatcher import dp
from telegram_bot.mini_api import Api
from telegram_bot.config import white_users, APP_HOST


@dp.message_handler(commands=['start'])
async def send_welcome(msg: types.Message):
    if msg.from_user.id not in white_users.values():
        return await msg.reply("Пробач, але я не можу тобі відповісти.")
    api_response = await Api([k for k, v in white_users.items() if v == msg.from_user.id][0])
    body = api_response["user"]
    await msg.answer(
        "Привіт, <i>%s</i>! Ось дані для авторизації:"
        "\nЛогін: <code>%s</code>\nПароль: <code>%s</code>\nТакож ось адреса для авторизації: %s" % (
            msg.from_user.full_name, body["username"], body["password"], APP_HOST
        )
    )
