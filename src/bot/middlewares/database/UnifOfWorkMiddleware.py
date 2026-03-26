import logging
from aiogram import BaseMiddleware
from sqlalchemy.ext.asyncio import AsyncSession


class UnitOfWorkMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        # Create
        session: AsyncSession
        session = data['db'] = data['db_maker']()

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