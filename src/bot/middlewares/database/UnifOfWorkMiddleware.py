import logging
from typing import cast

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession


class UnitOfWorkMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: Message | CallbackQuery, data):
        # Create
        session = data['db'] = cast(AsyncSession, data['db_maker']())

        # Inject
        try:
            result = await handler(event, data)

            await session.commit()

            return result
        except Exception as ex:
            await session.rollback()
            logging.warning('Rolled back DB session due to exception')
            raise ex
        finally:
            await session.close()