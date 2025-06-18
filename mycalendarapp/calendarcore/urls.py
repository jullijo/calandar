from django.urls import path
from . import views

urlpatterns = [
    path('week/', views.weekly_view, name='weekly_view'),
]
