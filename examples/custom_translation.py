"""
This is how you can translate the calendar to any language you want.
Or submit your translation on GitHub.
Do not forget to pass the translation name to the constructor.
"""

from telegram_bot_calendar import DetailedTelegramCalendar

your_translation_months = list('abcdefghijkl')
your_translation_days_of_week = list('yourtra')


class MyTranslationCalendar(DetailedTelegramCalendar):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.days_of_week['yourtransl'] = your_translation_days_of_week
        self.months['yourtransl'] = your_translation_months
