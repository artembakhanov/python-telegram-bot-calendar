import pytest
import sys, os
from datetime import date
from types import SimpleNamespace

myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')
from telegram_bot_calendar.base import YEAR, MONTH, DAY, max_date, min_date, TelegramCalendar, CB_CALENDAR


@pytest.mark.parametrize(('given', 'step', 'max_d'), [(date(2019, 5, 2), YEAR, date(2019, 12, 31)),
                                                      (date(1999, 12, 30), YEAR, date(1999, 12, 31)),
                                                      (date(2001, 1, 2), YEAR, date(2001, 12, 31)),
                                                      (date(2012, 5, 1), MONTH, date(2012, 5, 31)),
                                                      (date(2019, 9, 15), MONTH, date(2019, 9, 30)),
                                                      (date(2016, 2, 10), MONTH, date(2016, 2, 29)),
                                                      (date(2016, 2, 10), DAY, date(2016, 2, 10)),
                                                      ])
def test_max_date(given, step, max_d):
    assert max_date(given, step) == max_d


@pytest.mark.parametrize(('given', 'step', 'min_d'), [(date(2019, 5, 2), YEAR, date(2019, 1, 1)),
                                                      (date(1999, 12, 30), YEAR, date(1999, 1, 1)),
                                                      (date(2001, 1, 2), YEAR, date(2001, 1, 1)),
                                                      (date(2012, 5, 1), MONTH, date(2012, 5, 1)),
                                                      (date(2019, 9, 15), MONTH, date(2019, 9, 1)),
                                                      (date(2016, 2, 10), MONTH, date(2016, 2, 1)),
                                                      (date(2016, 2, 10), DAY, date(2016, 2, 10)),
                                                      ])
def test_min_date(given, step, min_d):
    assert min_date(given, step) == min_d


@pytest.mark.parametrize(('min_date', 'max_date', 'step', 'start', 'diff', 'period'),
                         [(date(2019, 11, 9), None, YEAR, date(2020, 1, 12), 2,
                           [date(2020, 1, 12), date(2021, 1, 12)])])
def test__get_period(min_date, max_date, step, start, diff, period):
    telegram_calendar = TelegramCalendar(min_date=min_date, max_date=max_date)

    assert telegram_calendar._get_period(step, start, diff) == period


@pytest.mark.parametrize(('calendar_id', 'callback_data', 'passed'),
                         [(0, 'cbcal_0_g_y_2017_1_13_238946419208856913', True),
                          (1, 'cbcal_0_g_y_2017_1_13_238946419208856913', False),
                          (1, 'cbcal_1_s_d_2016_8_25_971574741092873836', True),
                          (0, 'something_irrelevant', False),
                          (22, 'cbcal_22_n', True), ])
def test_func(calendar_id, callback_data, passed):
    assert TelegramCalendar.func(calendar_id)(SimpleNamespace(data=callback_data)) == passed
