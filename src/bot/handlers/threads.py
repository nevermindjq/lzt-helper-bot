import logging

from LOLZTEAM import Forum
from aiogram import Router, F
from aiogram.filters import Command, CommandObject
from aiogram.types import Message, InlineKeyboardButton, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

router = Router()

# Helpers
async def __show_threads(event: Message | CallbackQuery, lolz_forum: Forum, state: str):
    # Get lolz user id
    response = await lolz_forum.users.get('me')

    if response.status_code != 200:
        await event.answer('Ошибка при получении информации о пользователе. Повторите позже.')
        logging.error(f'Error getting information about user: {response.content.decode()}')
        return

    user_data = response.json()['user']

    # Get user threads
    response = await lolz_forum.threads.list(
        user_id=user_data['user_id'],
        state=state,
        limit=10
    )

    if response.status_code != 200:
        await event.answer('Ошибка при получении тем. Повторите позже.')
        logging.error(f'Error getting information about user: {response.content.decode()}')
        return

    threads_data = response.json()['threads']

    # Generate menu and answer
    text = 'Ваши темы. Нажмите для открытия/закрытия.'
    menu = InlineKeyboardBuilder()

    for thread in threads_data:
        menu.add(InlineKeyboardButton(
            text=f'{('❌' if thread['thread_is_closed'] else '✅')} {thread['thread_title']}',
            callback_data=f'threads:toggle:{state}:{thread['thread_id']}'
        ))

    menu.adjust(2)

    if isinstance(event, Message):
        await event.answer(
            text=text,
            reply_markup=menu.as_markup()
        )
    if isinstance(event, CallbackQuery):
        await event.message.edit_text(
            text=text,
            reply_markup=menu.as_markup()
        )

# Handlers
@router.message(Command('threads'))
async def threads(message: Message, command: CommandObject, lolz_forum: Forum):
    # Verify message
    args = command.args.split(' ') if command.args else []

    if len(args) != 1 or args[0] not in ['active', 'closed']:
        await message.reply('Не выбран тип тем: active/closed!')
        return

    await __show_threads(message, lolz_forum, args[0])

@router.callback_query(F.data.startswith('threads:toggle:'))
async def threads_toggle(callback: CallbackQuery, lolz_forum: Forum):
    args = callback.data.split(':')

    if len(args) != 4:
        await callback.answer('Произошла внутренняя ошибка. Повторите заново.')
        return

    state = 'active' if args[2] == 'closed' else 'closed'
    thread_id = args[3]

    # TODO: Create logic for close/open threads