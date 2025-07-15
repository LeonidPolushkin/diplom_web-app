from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from datetime import date
from .models import Reservations
from django.contrib import admin

@staff_member_required
def today_reservations_report(request):
    today = date.today()
    sort_by = request.GET.get('sort', 'reservation_time')
    order = request.GET.get('order', 'asc')

    valid_fields = ['reservation_time', 'table_number', 'status']
    if sort_by not in valid_fields:
        sort_by = 'reservation_time'

    order_prefix = '' if order == 'asc' else '-'
    ordering = f'{order_prefix}{sort_by}'

    reservations = Reservations.objects.filter(
        reservation_date=today
    ).exclude(status='Отменено').select_related('customer').order_by(ordering)

    return render(request, 'admin/today_reservations_report.html', {
        'reservations': reservations,
        'today': today,
        'sort_by': sort_by,
        'order': order,
        'site_header': admin.site.site_header,
    })