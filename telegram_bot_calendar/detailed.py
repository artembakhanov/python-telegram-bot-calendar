from calendar import monthrange
from telegram_bot_calendar.base import *

STEPS = {YEAR: MONTH, MONTH: DAY}
PREV_STEPS = {DAY: MONTH, MONTH: YEAR, YEAR: YEAR}
PREV_ACTIONS = {DAY: GOTO, MONTH: GOTO, YEAR: NOTHING}

class DetailedTelegramCalendar(TelegramCalendar):
    first_step = YEAR

    def __init__(self, calendar_id=0, current_date=None, additional_buttons=None, locale='en',
                 min_date=None, max_date=None, telethon=False, **kwargs):
        self.use_jdate = True if locale == 'fa' else False
        # Set a proper default date
        if current_date is None:
            if self.use_jdate:
                current_date = jdatetime.date.today()  # Use full module path
            else:
                current_date = date.today()
        super().__init__(calendar_id, current_date, additional_buttons, locale, min_date, max_date, telethon, **kwargs)

    def _build_years(self):
        years_num = self.size_year * self.size_year_column
        half_range = (years_num - 1) // 2
        start_year = self.current_date.year - half_range
        start = jdatetime.date(start_year, 1, 1) if self.use_jdate else date(start_year, 1, 1)
        years = self._get_period(YEAR, start, years_num)
        years_buttons = rows(
            [self._build_button(d.year if d else self.empty_year_button, SELECT if d else NOTHING, YEAR, d)
             for d in years],
            self.size_year
        )
        maxd = jdatetime.date(start.year + years_num - 1, 12, 29) if self.use_jdate else date(start.year + years_num - 1, 12, 31)
        nav_buttons = self._build_nav_buttons(YEAR, diff=relativedelta(years=years_num),
                                              mind=min_date(start, YEAR), maxd=maxd)
        self._keyboard = self._build_keyboard(years_buttons + nav_buttons)

    def _build_nav_buttons(self, step, diff, mind, maxd, *args, **kwargs):
        text = self.nav_buttons[step]
        month_name = self.months[self.locale][self.current_date.month - 1]
        data = {"year": str(self.current_date.year),
                "month": month_name,
                "day": str(self.current_date.day)}
        # Prev / Next pages
        if self.use_jdate:
            curr_page = self.current_date
            if step == YEAR:
                prev_page = self.current_date.replace(year=self.current_date.year - diff.years)
                next_page = self.current_date.replace(year=self.current_date.year + diff.years)
            elif step == MONTH:
                new_year = self.current_date.year
                new_month = self.current_date.month - diff.months
                if new_month < 1:
                    new_year -= 1
                    new_month += 12
                prev_page = self.current_date.replace(year=new_year, month=new_month)
                new_year = self.current_date.year
                new_month = self.current_date.month + diff.months
                if new_month > 12:
                    new_year += 1
                    new_month -= 12
                next_page = self.current_date.replace(year=new_year, month=new_month)
            else:  # DAY
                cur_tmp = self.current_date.togregorian() - relativedelta(days=diff.days)
                prev_page = jdatetime.date.fromgregorian(date=cur_tmp)
                cur_tmp = self.current_date.togregorian() + relativedelta(days=diff.days)
                next_page = jdatetime.date.fromgregorian(date=cur_tmp)
            prev_exists = (prev_page >= self.min_date) if self.min_date else True
            next_exists = (next_page <= self.max_date) if self.max_date else True
        else:
            curr_page = self.current_date
            prev_page = self.current_date - diff
            next_page = self.current_date + diff
            prev_exists = (prev_page >= self.min_date) if self.min_date else True
            next_exists = (next_page <= self.max_date) if self.max_date else True

        buttons = [[
            self._build_button(text[0].format(**data) if prev_exists else self.empty_nav_button,
                               GOTO if prev_exists else NOTHING, step, prev_page),
            self._build_button(text[1].format(**data),
                               PREV_ACTIONS[step], PREV_STEPS[step], curr_page),
            self._build_button(text[2].format(**data) if next_exists else self.empty_nav_button,
                               GOTO if next_exists else NOTHING, step, next_page),
        ]]
        return buttons

    def _process(self, call_data):
        params = call_data.split("_")
        # Ensure we have enough parameters
        expected_params = ["start", "calendar_id", "use_jdate", "action", "step", "year", "month", "day"]
        params = dict(zip(expected_params[:len(params)], params))
        if params['action'] == NOTHING:
            print("❌ ACTION: NOTHING - returning None")
            return None, None, None
        step = params['step']
        self.use_jdate = bool(int(params['use_jdate']))
        try:
            year = int(params['year'])
            month = int(params['month'])
            day = int(params['day'])
        except (ValueError, TypeError) as e:
            print(f"❌ ERROR parsing date: {e}")
            print(f"❌ Year: {params['year']}, Month: {params['month']}, Day: {params['day']}")
            return None, None, None
        if self.use_jdate:
            try:
                self.current_date = jdatetime.date(year, month, day)
            except Exception as e:
                print(f"❌ ERROR creating Jalali date: {e}")
                # Fallback to current date
                self.current_date = jdatetime.date.today()
        else:
            try:
                self.current_date = date(year, month, day)
            except Exception as e:
                print(f"❌ ERROR creating Gregorian date: {e}")
                # Fallback to current date
                self.current_date = date.today()
        if params['action'] == GOTO:
            self._build(step=step)
            return None, self._keyboard, step

        if params['action'] == SELECT:
            if step in STEPS:
                next_step = STEPS[step]
                self._build(step=next_step)
                return None, self._keyboard, next_step
            else:
                return self.current_date, None, step

    def _build(self, step=None):
        if not step:
            step = self.first_step
        self.step = step

        if step == YEAR:
            self._build_years()
        elif step == MONTH:
            self._build_months()
        else: # step == DAY
            self._build_days()

    def _build_months(self):
        months_buttons = []
        for i in range(1, 13):
            if self.use_jdate:
                d = jdatetime.date(self.current_date.year, i, 1)
            else:
                d = date(self.current_date.year, i, 1)
            if self._valid_date(d):
                month_name = self.months['fa'][i - 1] if self.use_jdate else self.months[self.locale][i - 1]
                months_buttons.append(self._build_button(month_name, SELECT, MONTH, d))
            else:
                months_buttons.append(self._build_button(self.empty_month_button, NOTHING))
        months_buttons = rows(months_buttons, self.size_month)
        if self.use_jdate:
            start = jdatetime.date(self.current_date.year, 1, 1)
            maxd = jdatetime.date(self.current_date.year, 12, 1)
        else:
            start = date(self.current_date.year, 1, 1)
            maxd = date(self.current_date.year, 12, 1)
        nav_buttons = self._build_nav_buttons(MONTH, diff=relativedelta(months=12),
                                              mind=min_date(start, MONTH), maxd=maxd)
        self._keyboard = self._build_keyboard(months_buttons + nav_buttons)

    def _build_days(self):
        if self.use_jdate:
            days_num = jdatetime.j_days_in_month[self.current_date.month - 1]
            if self.current_date.month == 12 and self.current_date.isleap():
                days_num += 1
            start = jdatetime.date(self.current_date.year, self.current_date.month, 1)
        else:
            days_num = monthrange(self.current_date.year, self.current_date.month)[1]
            start = date(self.current_date.year, self.current_date.month, 1)
        days = self._get_period(DAY, start, days_num)
        days_buttons = rows(
            [self._build_button(d.day if d else self.empty_day_button, SELECT if d else NOTHING, DAY, d)
             for d in days],
            self.size_day
        )
        locale_key = 'fa' if self.use_jdate else self.locale
        days_of_week_buttons = [[self._build_button(self.days_of_week[locale_key][i], NOTHING) for i in range(7)]]
        mind = min_date(start, MONTH)
        maxd_date = start.replace(day=days_num) if self.use_jdate else date(self.current_date.year, self.current_date.month,days_num)
        nav_buttons = self._build_nav_buttons(DAY, diff=relativedelta(months=1), mind=mind, maxd=max_date(maxd_date, MONTH))
        self._keyboard = self._build_keyboard(days_of_week_buttons + days_buttons + nav_buttons)
