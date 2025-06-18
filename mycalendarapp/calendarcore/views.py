from django.shortcuts import render
from .models import Shift
from datetime import timedelta, date

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