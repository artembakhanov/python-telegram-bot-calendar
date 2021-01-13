# python-telegram-bot-calendar

[![PyPI version](https://badge.fury.io/py/python-telegram-bot-calendar.svg)](https://badge.fury.io/py/python-telegram-bot-calendar)
[![CodeFactor](https://www.codefactor.io/repository/github/artembakhanov/python-telegram-bot-calendar/badge)](https://www.codefactor.io/repository/github/artembakhanov/python-telegram-bot-calendar)
![cock](https://github.com/artembakhanov/python-telegram-bot-calendar/workflows/Tests/badge.svg)

Very simple inline calendar for your bot.

<img src="https://i.gyazo.com/21d553c25481827b55174acfcf45259b.gif" style="zoom:67%;" />

# Getting Started

This library is tested on Python 3.6 and 3.7.

### Installation

```bash
pip install python-telegram-bot-calendar
```

### Usage

There is one main class - DetailedTelegramCalendar that can be used as follows. This is the example for [pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI) library. Other libraries are also supported.

```python
from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP

...
@bot.message_handler(commands=['start'])
def start(m):
    calendar, step = DetailedTelegramCalendar().build()
    bot.send_message(m.chat.id,
                     f"Select {LSTEP[step]}",
                     reply_markup=calendar)


@bot.callback_query_handler(func=DetailedTelegramCalendar.func())
def cal(c):
    result, key, step = DetailedTelegramCalendar().process(c.data)
    if not result and key:
        bot.edit_message_text(f"Select {LSTEP[step]}",
                              c.message.chat.id,
                              c.message.message_id,
                              reply_markup=key)
    elif result:
        bot.edit_message_text(f"You selected {result}",
                              c.message.chat.id,
                              c.message.message_id)
```

In start handler the calendar is created. Several arguments can be passed:

* `calendar_id` - small integer or string, used for calendar identification. It used when you need several different calendars (default - 0)
* `current_date` - `datetime.date`  object, initial date value (default - today date)
* `additional_buttons` - 1D list of buttons that will be added to the bottom of the calendar
* `locale` - either `en`, `ru`, or `eo`, can be added more
* `min_date` and `max_date` - both are used as min and max values for the calendar

As you can see, special function that is provided should be passed to callback query handler. It will automatically work. The function takes only one argument - `calendar_id` that is 0 by default.

In the body of the handler function you need to call process function on callback data. **WARNING!** You need to create the calendar object again if it was not saved before.

The function `process` return tuple of size 3 - `result`, `keyboard`, `step`.

* `result` - `datetime.date` object if user finished selecting. Otherwise `None`
* `keyboard` - inline keyboard markup if the result is not ready. Otherwise `None`
* `step` - `YEAR`, `MONTH`,  or `DAY` if not ready. `None` is also possible if there is no change in keyboard.

# Advanced use

### Several calendars

You can create as many calendars as you want. However, in order to handle them properly set different `calendar_id's` when  you want to distinguish them. Take a look at examples.

### Date ranges

In the class constructor `min_date` and `max_date` - both are used as min and max values for the calendar. If you add them, the calendar will not show undesired dates. Example:
<img src="https://github.com/artembakhanov/python-telegram-bot-calendar/raw/master/examples/images/5.png?raw=true" alt="3" style="zoom:67%;" />

### Custom style

You can also write your own code. One of the examples is redefining the steps order.

In the package you can find `WMonthTelegramCalendar` and `WYearTelegramCalendar` that start from day and month selecting, not from year.

You can also redefine style parameters. Example:

```python
class MyStyleCalendar(DetailedTelegramCalendar):
    # previous and next buttons style. they are emoji now!
    prev_button = "⬅️"
    next_button = "➡️"
    # you do not want empty cells when month and year are being selected
    empty_month_button = ""
    empty_year_button = ""
```

You will get:

 ![4](https://github.com/artembakhanov/python-telegram-bot-calendar/raw/master/examples/images/3.png)

### Custom Translation

```python
your_translation_months = list('abcdefghijkl')
your_translation_days_of_week = list('yourtra')

class MyTranslationCalendar(DetailedTelegramCalendar):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.days_of_week['yourtransl'] = your_translation_days_of_week
        self.months['yourtransl'] = your_translation_months
```

![5](https://github.com/artembakhanov/python-telegram-bot-calendar/raw/master/examples/images/4.png)

# Examples

* [simple_pytelegrambotapi.py](/examples/simple_pytelegrambotapi.py) - simple example with [pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI)
* [simple_aiogram.py](/examples/simple_aiogram.py) - simple example with [aiogram](https://github.com/aiogram/aiogram)
* [simple_telethon.py](/examples/simple_telethon.py) - simple example with [telethon](https://github.com/LonamiWebs/Telethon)
* [custom_translation.py](examples/custom_translation.py) - custom translation of calendar
* [date_ranges.py](/examples/date_ranges.py) - define date ranges for the bot
* [redefine_style.py](/examples/redefine_style.py) - simple example of redefining styles
* [several_calendars.py](/examples/several_calendars.py) - several calendars in one bot

# Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/yourFeature`)
3. Commit your Changes (`git commit -m 'Add some yourFeature'`)
4. Push to the Branch (`git push origin feature/yourFeature`)
5. Open a Pull Request

# Authors

* **Artem Bakhanov** - [@artembakhanov](https://github.com/artembakhanov)

# License

This project is licensed under the MIT License - see the [LICENSE](LICENSE.txt) file for details
