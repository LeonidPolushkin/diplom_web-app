from django.urls import path
from . import views
from . import admin_views

urlpatterns =[
    path('', views.reservation, name='reservation'),
    path('success_page', views.success_page, name='success_page'),
    path('api/reserved-times/', views.get_reserved_times, name='get_reserved_times'),

    # отчет для админки
    path('admin/report/today-reservations/', admin_views.today_reservations_report, name='today_reservations_report'),
]