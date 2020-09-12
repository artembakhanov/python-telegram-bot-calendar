import calendar
import json
import random
from datetime import date

from dateutil.relativedelta import relativedelta

from telegram_bot_calendar.static import MONTHS, DAYS_OF_WEEK

calendar.setfirstweekday(calendar.MONDAY)

CB_CALENDAR = "cbcal"

YEAR = 'y'
MONTH = 'm'
DAY = 'd'
SELECT = "s"
GOTO = "g"
NOTHING = "n"
LSTEP = {'y': 'year', 'm': 'month', 'd': 'day'}


class TelegramCalendar:
    months = MONTHS
    days_of_week = DAYS_OF_WEEK
    prev_button = "<<"
    next_button = ">>"
    middle_button_day = "{month} {year}"
    middle_button_month = "{year}"
    middle_button_year = " "
    back_to_button = "<<< {name}"
    empty_nav_button = "×"
    empty_day_button = " "
    empty_month_button = " "
    empty_year_button = " "
    size_year = 2
    size_year_column = 2
    size_month = 3
    size_day = 7
    size_additional_buttons = 2
    _keyboard = None
    step = None

    def __init__(self, calendar_id=0, current_date=None, additional_buttons=None, locale='en', min_date=None,
                 max_date=None, **kwargs):
        """

        :param date current_date: Where calendar starts, if None the current date is used
        :param view: The type of the calendar: either detailed, w/month, or w/year
        """
        if current_date is None: current_date = date.today()
        if min_date is None: min_date = date(1, 1, 1)
        if max_date is None: max_date = date(2999, 12, 31)

        self.calendar_id = calendar_id
        self.current_date = current_date
        self.locale = locale

        self.min_date = min_date
        self.max_date = max_date

        if not additional_buttons: additional_buttons = []
        self.additional_buttons = rows(additional_buttons, self.size_additional_buttons)

        self.prev_button_year = self.prev_button
        self.next_button_year = self.next_button
        self.prev_button_month = self.prev_button
        self.next_button_month = self.next_button
        self.prev_button_day = self.prev_button
        self.next_button_day = self.next_button

        self.nav_buttons = {
            YEAR: [self.prev_button_year, self.middle_button_year, self.next_button_year],
            MONTH: [self.prev_button_month, self.middle_button_month, self.next_button_month],
            DAY: [self.prev_button_day, self.middle_button_day, self.next_button_day],
        }

    @staticmethod
    def func(calendar_id=0):
        def inn(callback):
            start = CB_CALENDAR + "#" + str(calendar_id)
            return callback.data.startswith(start)

        return inn

    def build(self, **kwargs):
        if not self._keyboard:
            self._build(**kwargs)
        return self._keyboard, self.step

    def process(self, call_data, **kwargs):
        return self._process(call_data, **kwargs)

    def _build(self, *args, **kwargs):
        """
        Build the keyboard and set _keyboard.
        """

    def _process(self, call_data, *args, **kwargs):
        """
        :param call_data: callback data
        :return: (result, keyboard, message); if no result: result = None
        """

    def _build_callback(self, action, step, data, *args, is_random=False, **kwargs):
        if action == NOTHING:
            params = [CB_CALENDAR, str(self.calendar_id), action]
        else:
            data = list(map(str, data.timetuple()[:3]))
            params = [CB_CALENDAR, str(self.calendar_id), action, step] + data + [*kwargs.values()]

        # Random is used here to protect bots from being spammed by some 'smart' users.
        # Random callback data will not produce api errors "Message is not modified".
        # However, there is still a chance (1 in 1e18) that the same callbacks are created.
        salt = "#" + str(random.randint(1, 1e18)) if is_random else ""

        return "#".join(params) + salt

    def _build_button(self, text, action, step=None, data=None, is_random=False, **kwargs):
        return {
            'text': text,
            'callback_data': self._build_callback(action, step, data, is_random=is_random, **kwargs)
        }

    def _build_keyboard(self, buttons):
        return json.dumps({"inline_keyboard": buttons + self.additional_buttons})

    def _valid_date(self, d):
        return self.min_date <= d <= self.max_date

    def _get_period(self, step, start, diff, *args, **kwargs):
        lstep = LSTEP[step] + "s"
        dates = []

        empty_before = 0
        empty_after = 0

        for i in range(diff):
            n_date = start + relativedelta(**{lstep: i})
            if self.min_date > max_date(n_date, step):
                empty_before += 1
            elif self.max_date < min_date(n_date, step):
                empty_after += 1
            else:
                dates.append(n_date)
        return [None] * empty_before + dates + [None] * empty_after


def rows(buttons, row_size):
    return [buttons[i:i + row_size] for i in range(0, max(len(buttons) - row_size, 0) + 1, row_size)]


def max_date(d, step):
    if step == YEAR:
        return d.replace(month=12, day=31)
    elif step == MONTH:
        return d.replace(day=calendar.monthrange(d.year, d.month)[1])
    else:
        return d


def min_date(d, step):
    if step == YEAR:
        return d.replace(month=1, day=1)
    elif step == MONTH:
        return d.replace(day=1)
    else:
        return d
