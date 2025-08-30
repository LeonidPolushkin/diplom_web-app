from django.urls import path, include
from . import views
from . import admin_views
from rest_framework import routers
from .views import CustomersViewSet, ReservationsViewSet

router = routers.DefaultRouter()
router.register(r'customers', CustomersViewSet)
router.register(r'reservations', ReservationsViewSet)

urlpatterns =[
    path('', views.reservation, name='reservation'),
    path('success_page', views.success_page, name='success_page'),
    path('api/reserved-times/', views.get_reserved_times, name='get_reserved_times'),

    # отчет для админки
    path('admin/report/today-reservations/', admin_views.today_reservations_report, name='today_reservations_report'),
    path('api/', include(router.urls)), # все API-запросы будут начинаться с /api/
]