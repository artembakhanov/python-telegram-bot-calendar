"""
It absolutely the same for aiogram.
"""

from aiogram import Bot, Dispatcher, executor

from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP

bot = Bot(token="token")
dp = Dispatcher(bot)


@dp.message_handler(commands='start')
async def start(message):
    calendar, step = DetailedTelegramCalendar().build()
    await bot.send_message(message.chat.id,
                           f"Select {LSTEP[step]}",
                           reply_markup=calendar)


@dp.callback_query_handler(DetailedTelegramCalendar.func())
async def inline_kb_answer_callback_handler(query):
    result, key, step = DetailedTelegramCalendar().process(query.data)

    if not result and key:
        await bot.edit_message_text(f"Select {LSTEP[step]}",
                                    query.message.chat.id,
                                    query.message.message_id,
                                    reply_markup=key)
    elif result:
        await bot.edit_message_text(f"You selected {result}",
                                    query.message.chat.id,
                                    query.message.message_id)


executor.start_polling(dp, skip_updates=True)
