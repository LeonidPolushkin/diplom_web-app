from django.shortcuts import render, redirect
from .models import Customers, Reservations
from django.http import JsonResponse
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import CustomersSerializer, ReservationsSerializer

def reservation(request):
    if request.method == 'POST':
        # Получаем данные из формы
        client_name = request.POST.get('client_name')
        client_phone = request.POST.get('client_phone')
        client_email = request.POST.get('client_email')
        reservation_date = request.POST.get('reservation_date')
        reservation_time = request.POST.get('reservation_time')
        guest_count = request.POST.get('guest_count')
        comment = request.POST.get('comment')

        # Проверяем наличие клиента по телефону
        customer, created = Customers.objects.get_or_create(
            phone=client_phone,
            defaults={
                'name': client_name,
                'email': client_email
            }
        )

        # Создаем бронь
        reservation = Reservations.objects.create(
            customer=customer,
            reservation_date=reservation_date,
            reservation_time=reservation_time,
            status='В ожидании подтверждения',
            customer_count=guest_count,
            comments=comment,
        )

        return redirect('success_page')
    return render(request, 'reservation/reservation.html')

def success_page(request):
    return render(request, 'reservation/success_page.html')

def get_reserved_times(request):
    date = request.GET.get('date')
    if not date:
        return JsonResponse({'error': 'No date provided'}, status=400)

    total_tables = 14  # Общее количество столов

    # Только действующие брони
    reservations = Reservations.objects.filter(
        reservation_date=date
    ).exclude(status='Отменено')  # <-- исключаем отменённые

    time_counts = {}
    for r in reservations:
        time_str = r.reservation_time.strftime('%H:%M')
        time_counts[time_str] = time_counts.get(time_str, 0) + 1

    # Времена, где все столы заняты
    reserved_times = [time for time, count in time_counts.items() if count >= total_tables]

    return JsonResponse({'reserved_times': reserved_times})

# REST API
class CustomersViewSet(viewsets.ModelViewSet):
    queryset = Customers.objects.all()
    serializer_class = CustomersSerializer
    # фильтры
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name', 'phone', 'email']  # фильтруем по этим полям

class ReservationsViewSet(viewsets.ModelViewSet):
    queryset = Reservations.objects.all()
    serializer_class = ReservationsSerializer
    # фильтры
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['reservation_date', 'reservation_time', 'status', 'customer']