import os
import logging
from argparse import ArgumentError

from typing import Tuple
from aiogram import Bot, Dispatcher

from .commands import router_hello


def __configure_routers(dp: Dispatcher):
    logging.info('Configure routers')
    dp.include_routers(
        router_hello
    )

def __configure_services(dp: Dispatcher):
    pass

def create() -> Tuple[Bot, Dispatcher]:
    logging.info('Configuring application')
    token = os.getenv("TOKEN")

    if not token:
        raise ArgumentError(token, 'Telegram bot environment variables \'TOKEN\' is not set')

    bot = Bot(token=token)
    dp = Dispatcher()

    __configure_routers(dp)
    __configure_services(dp)

    return bot, dp

async def start(bot: Bot, dp: Dispatcher):
    logging.info('Starting application')
    await dp.start_polling(bot)