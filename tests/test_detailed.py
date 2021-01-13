import json
import os
import sys
from datetime import date

import pytest
from dateutil.relativedelta import relativedelta

from telegram_bot_calendar import DAY, MONTH, YEAR
from telegram_bot_calendar.detailed import DetailedTelegramCalendar, NOTHING

myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')


# todo: fix this test to properly check generated keyboard
@pytest.mark.parametrize(('callback_data', 'result', 'key', 'step'),
                         [('cbcal_0_s_m_2021_11_13_726706365801178150', None, None, DAY),
                          ('cbcal_0_s_d_2021_11_13_726706365801178150', date(2021, 11, 13), None, DAY),
                          ('cbcal_0_s_y_2020_1_1_726702345801178150', None, None, MONTH),
                          ('cbcal_0_n_726702345801178150', None, None, None),
                          ('cbcal_0_g_m_2022_5_7_726702345801178150', None, None, MONTH)])
def test_process(callback_data, result, key, step):
    calendar = DetailedTelegramCalendar(current_date=date(2021, 1, 12))
    result_, _, step_ = calendar.process(callback_data)
    assert result_ == result and step_ == step


@pytest.mark.parametrize(
    ('step', 'start', 'diff', 'mind', 'maxd', 'min_button_date', 'max_button_date', 'result_buttons'),
    [
        (
                MONTH, date(2021, 1, 12), relativedelta(months=12), date(2021, 1, 1), date(2021, 3, 2), date(2021, 1, 1),
                date(2021, 3, 2),
                [{'text': "×", "callback_data": "cbcal_0_n"},
                 {'text': "2021", "callback_data": "cbcal_0_g_y_2021_1_12"},
                 {'text': "×", "callback_data": "cbcal_0_n"}]
        ),
        (
                MONTH, date(2021, 1, 12), relativedelta(months=12), date(2021, 1, 1), date(2022, 1, 1), date(2021, 1, 1),
                date(2021, 12, 1),
                [{'text': "×", "callback_data": "cbcal_0_n"},
                 {'text': "2021", "callback_data": "cbcal_0_g_y_2021_1_12"},
                 {'text': ">>", "callback_data": "cbcal_0_g_m_2022_1_1"}]
        ),
(
                YEAR, date(2021, 5, 12), relativedelta(years=4), date(2018, 5, 12), date(2023, 5, 12), date(2019, 5, 12),
                date(2019, 5, 12),
                [{'text': "<<", "callback_data": "cbcal_0_g_y_2017_5_12"},
                 {'text': " ", "callback_data": "cbcal_0_n"},
                 {'text': ">>", "callback_data": "cbcal_0_g_y_2025_5_12"}]
        )
    ])
def test__build_nav_buttons(step, start, diff, mind, maxd, min_button_date, max_button_date, result_buttons):
    calendar = DetailedTelegramCalendar(current_date=start, min_date=mind, max_date=maxd)
    buttons = calendar._build_nav_buttons(step, diff, min_button_date, max_button_date)

    result = True
    print(buttons[0])
    for i, button in enumerate(buttons[0]):
        if button['text'] != result_buttons[i]['text'] or button['callback_data'].startswith(result_buttons[i]['text']):
            result = False

    assert result
