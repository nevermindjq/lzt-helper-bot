import logging
from typing import cast

from LOLZTEAM import Forum
from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.entities import User


class LolzTeamApiMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: Message | CallbackQuery, data):
        user: User = await cast(AsyncSession, data['db']).get(User, event.from_user.id)

        if user.api_key:
            try:
                data['lolz_forum'] = Forum(
                    token=user.api_key,
                    language='ru'
                )
            except Exception as ex:
                logging.error(f'User API Token is invalid.', user.id, user.api_key, exc_info=ex)
        else:
            data['lolz_forum'] = None

        return await handler(event, data)