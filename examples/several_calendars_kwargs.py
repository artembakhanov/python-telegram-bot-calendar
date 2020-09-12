"""
This is the simplest example of how to use several calendars in one.
This example is not realistic, but imagine that you need 2 calendars: one russian and one english.

It can be used with different date ranges, for example when you need calendar for specifying a person's birth date
and another one for specifying booking date. These two have different properties and hence need to be handled
differently.

Also you can transfer data to second calendar using kwargs.
"""

from telebot import TeleBot

from telegram_bot_calendar import WMonthTelegramCalendar, LSTEP

bot = TeleBot("token")


@bot.message_handler(commands=['start'])
def start(m):
    calendar, step = WMonthTelegramCalendar(calendar_id=1).build()
    bot.send_message(m.chat.id,
                     f"Select {LSTEP[step]}",
                     reply_markup=calendar)


def select_another_date(m, date):
    calendar, step = WMonthTelegramCalendar(calendar_id=2).build(some_date=date)
    bot.send_message(m.chat.id,
                     f"Select {LSTEP[step]}",
                     reply_markup=calendar)


@bot.callback_query_handler(func=WMonthTelegramCalendar.func(calendar_id=1))
def cal1(c):
    result, key, step = WMonthTelegramCalendar().process(c.data)
    if not result and key:
        bot.edit_message_text(f"Select {LSTEP[step]}",
                              c.message.chat.id,
                              c.message.message_id,
                              reply_markup=key)
    elif result:
        bot.edit_message_text(f"You selected {result}",
                              c.message.chat.id,
                              c.message.message_id)

    select_another_date(c.message, str(result))


@bot.callback_query_handler(func=WMonthTelegramCalendar().func(calendar_id=2))
def cal2(c):
    result, key, step = WMonthTelegramCalendar().process(c.data, some_date='')
    if not result and key:
        bot.edit_message_text(f"Select {LSTEP[step]}",
                              c.message.chat.id,
                              c.message.message_id,
                              reply_markup=key)
    elif result:
        bot.edit_message_text(f"You selected {result[0]}",
                              c.message.chat.id,
                              c.message.message_id)

        bot.send_message(c.message.chat.id, f"And i saved for you this date {result[-1]['some_date']}")


bot.polling()
