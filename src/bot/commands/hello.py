from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message


router = Router()

@router.message(Command('start'))
async def hello(message: Message):
    await message.reply(f'Hello, {message.from_user.username}!')