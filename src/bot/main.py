import os
import logging
from argparse import ArgumentError
from typing import Tuple
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage, SimpleEventIsolation
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, AsyncSession


def __configure_routers(dp: Dispatcher):
    logging.info('Configure routers')

    from .commands import router_hello

    dp.include_routers(
        router_hello
    )

def __configure_services(dp: Dispatcher):
    # Database
    from src.database import create_engine, create_maker
    from .middlewares import UnitOfWorkMiddleware
    dp['db_engine'] = create_engine()
    dp['db_maker'] = create_maker(dp['db_engine'])
    dp.update.middleware(UnitOfWorkMiddleware())

    #
    pass

def create() -> Tuple[Bot, Dispatcher]:
    logging.info('Configuring application')
    token = os.getenv("TOKEN")

    if not token:
        raise ArgumentError(token, 'Telegram bot environment variables \'TOKEN\' is not set')

    bot = Bot(token=token)

    dp = Dispatcher(
        storage=MemoryStorage(),
        events_isolation=SimpleEventIsolation()
    )

    __configure_routers(dp)
    __configure_services(dp)

    return bot, dp

async def start(bot: Bot, dp: Dispatcher):
    logging.info('Starting application')

    try:
        await dp.start_polling(bot)
    finally:
        # Database
        db_maker: async_sessionmaker[AsyncSession]  = dp.get('db_maker')
        if db_maker :
            await db_maker.class_.close_all()

        db_engine: AsyncEngine = dp.get('db_engine')
        if db_engine:
            await db_engine.dispose()

        # Bot
        await dp.storage.close()
        await bot.session.close()