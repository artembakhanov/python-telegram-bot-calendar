from telegram_bot_calendar.base import MONTH
from telegram_bot_calendar.detailed import DetailedTelegramCalendar


class WYearTelegramCalendar(DetailedTelegramCalendar):
    first_step = MONTH
