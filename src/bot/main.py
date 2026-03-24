import logging
from os import environ
from typing import Tuple
from aiogram import Bot, Dispatcher

from .commands import router_hello


def create() -> Tuple[Bot, Dispatcher]:
    logging.info('Configuring application')

    bot = Bot(token=environ.get("TOKEN"))
    dp = Dispatcher()

    logging.info('Configure routers')
    dp.include_routers(
        router_hello
    )

    return bot, dp

async def start(bot: Bot, dp: Dispatcher):
    logging.info('Starting application')
    await dp.start_polling(bot)