import sys
import asyncio
import logging
from dotenv import load_dotenv

from bot import create, start


def __configure_environment():
    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s] [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        encoding="utf-8",
        handlers=[
            logging.FileHandler("app.log", encoding="utf-8"),
            logging.StreamHandler(sys.stdout)
        ]
    )

    logging.info('Configure environment')
    load_dotenv()

async def main():
    __configure_environment()
    bot, dp = create()

    try:
        await start(bot, dp)
    except Exception as ex:
        logging.warning("Unknown exception", ex)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info('Stopping application')