from telegram_bot_calendar.base import DAY
from telegram_bot_calendar.detailed import DetailedTelegramCalendar


class WMonthTelegramCalendar(DetailedTelegramCalendar):
    first_step = DAY
