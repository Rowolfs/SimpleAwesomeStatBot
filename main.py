import asyncio
import logging
import sys
import db_controls
from os import getenv

from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.utils.markdown import hbold

# Bot token can be obtained via https://t.me/BotFather
Key = open("key")
TOKEN = Key.readline()
Key.close()

# All handlers should be attached to the Router (or Dispatcher)
dp = Dispatcher()





@dp.message(CommandStart())
async def start_handler(message: types.Message) -> None:
    chat_id = db_controls.select("BotDB", "chats", "chat_id", "chat_id", message.chat.id)
    if message.chat.id == chat_id:
        await message.answer("Этот чат уже добавлен")
    else:

        chat_attributes = {
            "chat_id": "INTEGER UNIQUE",
            "message_count": "INTEGER",

        }
        insert_values = {
            "chat_id": message.chat.id,
            "message_count": 0,

        }
        db_controls.connect_table("BotDB", "chats", chat_attributes)
        db_controls.insert("BotDB", "chats", insert_values)
        await message.answer("Начал считать")


@dp.message(Command("count"))
async def count_handler(message: types.Message) -> None:
    count = db_controls.select("BotDB", "chats", "message_count", "chat_id", message.chat.id)
    await message.answer("Количество сообшений которые я насчитал: "+str(count))

@dp.message()
async def message_handler(message: types.Message) -> None:
    chat_id = db_controls.select("BotDB", "chats", "chat_id", "chat_id", message.chat.id)
    if message.chat.id == chat_id:
        count = db_controls.select("BotDB", "chats", "message_count", "chat_id", message.chat.id)
        db_controls.update("BotDB", "chats", "message_count",count+1,"chat_id", message.chat.id)


async def main() -> None:
    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
