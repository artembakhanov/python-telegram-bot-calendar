"""
Example using telethon.
"""

from telethon import Button, TelegramClient, events
import telegram_bot_calendar.base
from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP

import json
from typing import List, Dict, Callable

api_id = 1234567
api_hash = "api-hash-here"
bot_token = "bot-token-here"

bot = TelegramClient("bot", api_id, api_hash)


def build_buttons(markup: str) -> List[List[Button]]:
    # Telethon uses Telegram's MTProto protocol directly
    # instead of relying on the Bot API. This means
    # that telethon doesn't send or recieve data in json
    # and so we have to parse the text and callback data
    # of buttons to proper objects.

    button_markup_data: Dict = json.loads(markup)

    buttons: List[List[Button]] = []
    for button_row in button_markup_data["inline_keyboard"]:
        button_row: List[Dict]
        buttons.append(
            [
                Button.inline(text=str(but["text"]), data=but["callback_data"])
                for but in button_row
            ]
        )

    return buttons


def callback_filter(calendar_id=0) -> Callable:
    # Due to differences in design, we cannot use
    # DetailedTelegramCalendar.func() directly for telethon

    def inner(callback_data: bytes) -> bool:
        start = telegram_bot_calendar.base.CB_CALENDAR + "_" + str(calendar_id)
        return callback_data.decode("utf-8").startswith(start)

    return inner


@bot.on(events.NewMessage(pattern="/start"))
async def reply_handler(event):
    calendar, step = DetailedTelegramCalendar().build()
    await event.respond(f"Select {LSTEP[step]}", buttons=build_buttons(calendar))


@bot.on(events.CallbackQuery(pattern=callback_filter()))
async def calendar_handler(event):
    result, key, step = DetailedTelegramCalendar().process(event.data.decode("utf-8"))

    if not result and key:
        await event.edit(f"Select {LSTEP[step]}", buttons=build_buttons(key))
    elif result:
        await event.edit(f"You selected {result}")


bot.start(bot_token=bot_token)
with bot:
    bot.run_until_disconnected()
