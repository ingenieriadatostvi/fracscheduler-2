import calendar
from datetime import datetime

from flask import render_template, request

from . import controllers
from .calendar_view import choose_utils, build_months, fraction_colors
from models import (
    apartament_maintenance_path,
    apartament_weekday_calendar_starts,
    apartament_type,
)
from utils.hollydays import regular_hollydays_dic, snow_hollydays_dic


@controllers.route('/hunt_fraction')
def hunt_fraction():
    date_str = request.args.get('hunter_date')
    apartment = request.args.get('apartament', 204, type=int)

    if not date_str:
        return "No date provided", 400

    maintenance_path = apartament_maintenance_path.get(apartment, 1)
    weekday_start = apartament_weekday_calendar_starts.get(apartment, 1)
    _, _, hunter = choose_utils(apartment)

    try:
        wish = datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        return "Invalid date format", 400

    result = hunter(
        wish.year, wish.month, wish.day,
        weekday_start, maintenance_path
    )

    if isinstance(result, str):
        return result, 404

    # rebuild all data for that year
    idx_maker, unfract_list, _ = choose_utils(apartment)
    frac_idx = idx_maker(wish.year, weekday_start, maintenance_path)
    frac_prev = idx_maker(wish.year - 1, weekday_start, maintenance_path)
    frac_next = idx_maker(wish.year + 1, weekday_start, maintenance_path)

    unf_curr = unfract_list(wish.year, weekday_start, maintenance_path)
    unf_prev = unfract_list(wish.year - 1, weekday_start, maintenance_path)
    unf_next = unfract_list(wish.year + 1, weekday_start, maintenance_path)

    apt_type = apartament_type.get(apartment, "regular")
    months = build_months(wish.year, apt_type)

    display_cal = calendar.Calendar(firstweekday=0)
    prev_dec = display_cal.monthdayscalendar(wish.year - 1, 12)
    day_names = [calendar.day_abbr[i] for i in range(7)]

    golden_holidays = (
        snow_hollydays_dic(wish.year) if apt_type == "snow"
        else regular_hollydays_dic(wish.year)
    )

    return render_template(
        'calendar.html',
        year=wish.year,
        apt_type=apt_type,
        apartament=apartment,
        available_apartaments=sorted(apartament_maintenance_path.keys()),
        day_names=day_names,
        calendar=calendar,
        fraction_colors=fraction_colors,
        datetime=datetime,
        months_with_index=months,
        previous_december=prev_dec,
        fractional_indices=frac_idx,
        fractional_indices_prev=frac_prev,
        fractional_indices_next=frac_next,
        unfractional_dates=unf_curr,
        unfractional_dates_prev=unf_prev,
        unfractional_dates_next=unf_next,
        selected_fractions=[result[0]],
        golden_holidays=golden_holidays,
    )
