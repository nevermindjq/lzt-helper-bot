from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.entities import User


class AuthenticationMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: Message | CallbackQuery, data):
        db: AsyncSession = data['db']
        user_id = event.from_user.id
        user: User = await db.get(User, user_id)
        is_first = False

        if not user:
            is_first = True
            user = User(id=user_id)
            db.add(user)

        data['user'] = user
        data['user_is_first'] = is_first

        return await handler(event, data)