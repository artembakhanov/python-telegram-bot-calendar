import calendar
import json
import random
from datetime import date

from dateutil.relativedelta import relativedelta

try:
    from telethon import Button

    TELETHON_INSTALLED = True
except ImportError:
    TELETHON_INSTALLED = False

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
                 max_date=None, telethon=False, is_random=True, **kwargs):
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

        self.telethon = telethon
        if self.telethon and not TELETHON_INSTALLED:
            raise ImportError(
                "Telethon is not installed. Please install telethon or use pip install python-telegram-bot-calendar[telethon]")
        # whether to add random numbers to callbacks
        self.is_random = is_random

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
    def func(calendar_id=0, telethon=False):
        def inn(callback):
            start = CB_CALENDAR + "_" + str(calendar_id)
            return callback.decode("utf-8").startswith(start) if telethon else callback.data.startswith(start)

        return inn

    def build(self):
        if not self._keyboard:
            self._build()
        return self._keyboard, self.step

    def process(self, call_data):
        return self._process(call_data)

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
            params = [CB_CALENDAR, str(self.calendar_id), action, step] + data

        # Random is used here to protect bots from being spammed by some 'smart' users.
        # Random callback data will not produce api errors "Message is not modified".
        # However, there is still a chance (1 in 1e18) that the same callbacks are created.
        salt = "_" + str(random.randint(1, 1e18)) if is_random else ""

        return "_".join(params) + salt

    def _build_button(self, text, action, step=None, data=None, is_random=False, **kwargs):
        if self.telethon:
            return Button.inline(text=str(text), data=self._build_callback(action, step, data, is_random=is_random))
        else:
            return {
                'text': text,
                'callback_data': self._build_callback(action, step, data, is_random=is_random)
            }

    def _build_keyboard(self, buttons):
        if self.telethon:
            return buttons
        return self._build_json_keyboard(buttons)

    def _build_json_keyboard(self, buttons):
        """
        Build keyboard in json to send to Telegram API over HTTP.
        """
        return json.dumps({"inline_keyboard": buttons + self.additional_buttons})

    def _valid_date(self, d):
        return self.min_date <= d <= self.max_date

    def _get_period(self, step, start, diff, *args, **kwargs):
        """
        Used for getting period of dates with a given step, start date and difference.
        It allows to create empty dates if they are not in the given range.
        """
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
    """
    Build rows for the keyboard. Divides list of buttons to list of lists of buttons.

    """
    return [buttons[i:i + row_size] for i in range(0, max(len(buttons) - row_size, 0) + 1, row_size)]


def max_date(d, step):
    """
    Returns the "biggest" possible date for a given step.
    It is used for navigations buttons when it is needed to check if prev/next page exists.

    :param d datetime
    :param step current step
    """
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
