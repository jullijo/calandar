from django.urls import path
from . import views

urlpatterns = [
    path('week/', views.weekly_view, name='weekly_view'),
    #path('calendar/', views.calendar_view, name='calendar_view'),
    path('calendar/', views.monthly_calendar_view, name='calendar'),
    path('calendar/<int:year>/<int:month>/', views.monthly_calendar_view, name='calendar_by_month'),
]
