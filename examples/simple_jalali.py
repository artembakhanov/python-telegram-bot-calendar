"""
This is an example of the Jalali calendar usage with pyTelegramBotAPI.
"""

from telebot import TeleBot

from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP

bot = TeleBot("token")

calendar = DetailedTelegramCalendar(locale='fa')


@bot.message_handler(commands=['start'])
def start(m):
    key, step = calendar.build()
    bot.send_message(m.chat.id,
                     f"Select {LSTEP[step]}",
                     reply_markup=key)


@bot.callback_query_handler(func=calendar.func())
def cal(c):
    result, key, step = calendar.process(c.data)
    if not result and key:
        bot.edit_message_text(f"Select {LSTEP[step]}",
                              c.message.chat.id,
                              c.message.message_id,
                              reply_markup=key)
    elif result:
        bot.edit_message_text(f"You selected {result}",
                              c.message.chat.id,
                              c.message.message_id)


bot.polling()
