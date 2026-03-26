import logging

from LOLZTEAM.Client.Base.Exceptions import BAD_TOKEN
from aiogram import Router
from aiogram.filters import ExceptionTypeFilter
from aiogram.types import ErrorEvent


router = Router()
logger = logging.getLogger(__name__)

# Helpers
async def __get_user_id_and_notify_him(event: ErrorEvent, text: str) -> int:
    if event.update.message:
        await event.update.message.answer(text)
        return event.update.message.from_user.id

    if event.update.callback_query:
        await event.update.callback_query.answer(text)
        return event.update.callback_query.from_user.id

    return None

def __log_critical_unknown_update(event: ErrorEvent):
    logger.critical(
        'Unknown update type. User ID is not extracted',
        extra={
            'update.id': event.update.update_id
            # TODO: Append 'update.type' extra
        }
    )

# Handlers
@router.error(ExceptionTypeFilter(BAD_TOKEN))
async def error_lolz_bad_token(event: ErrorEvent):
    user_id: int | None = await __get_user_id_and_notify_him(
        event,
        'Ваш API ключ неверный. Обновите его.'
    )

    if not user_id:
        __log_critical_unknown_update(event)

    logger.warning(
        'Invalid LolzTeam API token.',
        extra={
            'user.id': user_id
        }
    )

@router.errors()
async def errors(event: ErrorEvent):
    user_id: int | None = await __get_user_id_and_notify_him(
        event,
        'Произошла внутренняя ошибка. Повторите позже.'
    )

    if not user_id:
        __log_critical_unknown_update(event)

    logger.critical(
        'Internal exception',
        exc_info=event.exception,
        extra={
            'user.id': user_id
        }
    )