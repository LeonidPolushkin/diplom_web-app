from rest_framework import serializers
from .models import Customers, Reservations

class CustomersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customers
        fields = '__all__'  # все поля

class ReservationsSerializer(serializers.ModelSerializer):
    customer = CustomersSerializer(read_only=True)  # выводим данные клиента

    class Meta:
        model = Reservations
        fields = '__all__'
