from django import forms
from .models import Reservations, Tables

class ReservationAdminForm(forms.ModelForm):
    class Meta:
        model = Reservations
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        instance = kwargs.get('instance')
        if instance and instance.reservation_date and instance.reservation_time:
            # Получаем все занятые столы на это время, исключая отменённые
            reserved_tables = Reservations.objects.filter(
                reservation_date=instance.reservation_date,
                reservation_time=instance.reservation_time
            ).exclude(status='Отменено').exclude(pk=instance.pk).values_list('table_number', flat=True)

            # Доступные столы
            available_tables = Tables.objects.exclude(pk__in=reserved_tables)

            self.fields['table_number'].queryset = available_tables