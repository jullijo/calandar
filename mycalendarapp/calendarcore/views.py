from django.shortcuts import render
from .models import Shift
from datetime import timedelta, date
from calendar import Calendar, month_name

def weekly_view(request):
    shifts = Shift.objects.order_by('date')
    return render(request, "calendarcore/weekly.html", {"shifts": shifts})

def get_upcoming_week():
    today = date.today()
    # Start on Friday if today is before Friday
    weekday = today.weekday()  # Monday = 0 ... Sunday = 6
    start = today + timedelta((4 - weekday) % 7)  # 4 = Friday
    return [start + timedelta(days=i) for i in range(3)]  # Fri-Sun

def calendar_view(request):
    days = get_upcoming_week()
    shifts = Shift.objects.filter(date__in=days).select_related('worker')

    # Structure: { date: { 'morning': Worker, 'evening': Worker } }
    schedule = {day: {'morning': None, 'evening': None} for day in days}
    for shift in shifts:
        schedule[shift.date][shift.time_of_day] = shift.worker

    return render(request, "calendarcore/calendar.html", {
        "schedule": schedule,
        "days": days,
    })

def monthly_calendar_view(request, year=None, month=None):
    today = date.today()
    year = int(year) if year else today.year
    month = int(month) if month else today.month

    cal = Calendar(firstweekday=6)
    month_days = cal.monthdatescalendar(year, month)

    # Previous and next month
    prev_month = (month - 1) or 12
    prev_year = year - 1 if prev_month == 12 else year
    next_month = (month % 12) + 1
    next_year = year + 1 if next_month == 1 else year

    # Shifts
    month_start = date(year, month, 1)
    next_month_start = date(next_year, next_month, 1)
    shifts = Shift.objects.filter(date__gte=month_start, date__lt=next_month_start).select_related('worker')
    shift_map = {}
    for shift in shifts:
        shift_map.setdefault(shift.date, []).append(shift)

    return render(request, "calendarcore/monthly_calendar.html", {
        "year": year,
        "month": month,
        "month_name": month_name[month],
        "month_days": month_days,
        "shift_map": shift_map,
        "day_names": ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'],
        "prev_year": prev_year,
        "prev_month": prev_month,
        "next_year": next_year,
        "next_month": next_month,
    })