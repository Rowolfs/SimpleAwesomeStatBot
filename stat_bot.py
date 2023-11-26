import asyncio
import logging
import sqlite3
import sys
import db_controls
from os import getenv

from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.utils.markdown import hbold

# Bot token can be obtained via https://t.me/BotFather
Key = open("Token.txt")
TOKEN = Key.readline()
Key.close()

# All handlers should be attached to the Router (or Dispatcher)
dp = Dispatcher()
# Initialize Bot instance with a default parse mode which will be passed to all API calls
bot = Bot(TOKEN, parse_mode=ParseMode.HTML)


@dp.message(CommandStart())
async def start_handler(message: types.Message) -> None:
    chat_id = db_controls.select("data\BotDB", "chats", "chat_id", "chat_id", message.chat.id)

    # проверка на наличие чата в бд
    if message.chat.id == chat_id:
        await message.answer("Этот чат уже добавлен")
    else:

        chat_attributes = {
            "chat_id": "INTEGER UNIQUE",
            "start_message_id": "INTEGER",
            "message_count": "INTEGER",
            "start_date_processing": "TEXT",

        }
        insert_values = {
            "chat_id": message.chat.id,
            "message_count": 0,
            "start_date_processing": message.date.strftime("%d.%m.%Y"),
            "start_message_id": message.message_id
        }
        db_controls.connect_table("data\BotDB", "chats", chat_attributes)
        db_controls.insert("data\BotDB", "chats", insert_values)
        await message.answer(
            "Привет я бот сделанный Ромой пока я умею немного (считать сообщения) но он вложил меня много труда поютому я тут и да я начал считать")


@dp.message(Command("count"))
async def count_handler(message: types.Message) -> None:
    count = db_controls.select("data\BotDB", "chats", "message_count", "chat_id", message.chat.id)
    date = db_controls.select("data\BotDB", "chats", "start_date_processing", "chat_id", message.chat.id)
    await message.answer("Количество сообшений которые я насчитал: " + str(count) + " начиная с " + date)


@dp.message(Command("start_message_id"))
async def start_message_id_handler(message: types.Message) -> None:
    start_message_id = db_controls.select("data\BotDB", "chats", "start_message_id", "chat_id", message.chat.id)
    await bot.send_message(message.chat.id, "Команда c которой я начал считать", reply_to_message_id=start_message_id)


@dp.message()
async def message_handler(message: types.Message) -> None:
    count = db_controls.select("data\BotDB", "chats", "message_count", "chat_id", message.chat.id)
    if count is not None:
        db_controls.update("data\BotDB", "chats", "message_count", count + 1, "chat_id", message.chat.id)


async def main() -> None:
    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
