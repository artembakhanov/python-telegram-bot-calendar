import asyncio
from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP

api_id = xxxx
api_hash = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
token = 'xxxxxxxxx:xxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

app = Client("Bot", bot_token=token, api_hash=api_hash, api_id=api_id)

@app.on_message(filters.command(['start'], prefixes=['/']))
async def start(client, message):
    try:
        calendar, step = DetailedTelegramCalendar(pyrogram=True).build()
        await message.reply(f"Select {LSTEP[step]}", reply_markup=calendar)
    except FloodWait as e:
        await asyncio.sleep(e.value)
    except Exception as err:
        await async_error(f'[start] Err: {err}')

@app.on_callback_query(DetailedTelegramCalendar.func(pyrogram=True))
async def inline_kb_answer_callback_handler(client, query):
    result, key, step = DetailedTelegramCalendar(pyrogram=True).process(query.data)
    message = query.message
    if not result and key:
        await message.edit(f"Select {LSTEP[step]}", reply_markup=key)
    elif result:
        await message.edit(f"You selected {result}")
        
app.run()