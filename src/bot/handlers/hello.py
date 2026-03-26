from LOLZTEAM import Forum
from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandObject
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import User


router = Router()

@router.message(Command('start'))
async def hello(message: Message, lolz_forum: Forum | None):
    if lolz_forum:
        response = await lolz_forum.users.get('me')
        data = response.json()['user']

        await message.reply(f'Hello, {data['username']}!')
    else:
        await message.reply(f'Hello, {message.from_user.username}!', parse_mode=ParseMode.HTML)

@router.message(Command('set_api_key'))
async def set_api(message: Message, command: CommandObject, db: AsyncSession):
    # Verify message
    args = command.args.split(' ') if command.args else []

    if len(args) != 1:
        await message.reply('API Ключ не найден')
        return

    key: str = args[0]

    # Verify token
    Forum(token=key)

    # Update
    user: User = await db.get(User, message.from_user.id)
    user.api_key = key

    await message.delete()
    await message.answer('API Ключ установлен')