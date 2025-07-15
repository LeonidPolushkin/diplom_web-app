from django.contrib import admin
from .models import Actions, Administrators, Customers, Reservations, Tables
from .forms import ReservationAdminForm

admin.site.site_header = "Администрирование Бронирований"
admin.site.site_title = "Панель управления"
admin.site.index_title = "Добро пожаловать в панель администрации"

@admin.register(Actions)
class ActionsAdmin(admin.ModelAdmin):
    list_display = ('id', 'administrator', 'reservation_number', 'performed_action', 'created_at')
    list_filter = ('performed_action', 'created_at', 'administrator')  # Фильтрация по типу действия, дате и администратору
    search_fields = ('administrator__name', 'administrator__login', 'reservation_number__reservation_number')  # Поиск по администратору и номеру брони
    readonly_fields = ('created_at',)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "reservation_number":
            status_order = ['В ожидании подтверждения', 'Подтверждено', 'Отменено']
            from django.db.models import Case, When, IntegerField

            kwargs["queryset"] = Reservations.objects.annotate(
                status_ordering=Case(
                    *[When(status=s, then=i) for i, s in enumerate(status_order)],
                    output_field=IntegerField()
                )
            ).order_by('status_ordering', 'reservation_date', 'reservation_time')

        return super().formfield_for_foreignkey(db_field, request, **kwargs)

@admin.register(Administrators)
class AdministratorsAdmin(admin.ModelAdmin):
    list_display = ('id', 'login', 'name', 'phone', 'email')
    search_fields = ('login', 'name', 'phone', 'email')  # Поиск по логину, имени, телефону и email

@admin.register(Customers)
class CustomersAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone', 'email','staff_comment', 'created_at')
    search_fields = ('name', 'phone', 'email', 'created_at', 'staff_comment')  # Поиск по имени, телефону, email, дате создания и комментарию персонала
    readonly_fields = ('created_at',)

@admin.register(Reservations)
class ReservationsAdmin(admin.ModelAdmin):
    form = ReservationAdminForm
    list_display = ('reservation_number', 'customer', 'table_number', 'reservation_date', 'reservation_time', 'status')
    list_filter = ('status', 'table_number')  # Фильтрация по статусу, дате бронирования и столику
    search_fields = ('customer__name', 'reservation_number', 'reservation_date')  # Поиск по имени клиента, номеру брони и дате брони
    readonly_fields = ('created_at',)

@admin.register(Tables)
class TablesAdmin(admin.ModelAdmin):
    list_display = ('number', 'capacity', 'description')
    list_filter = ('capacity',)  # Фильтрация по количеству мест
    search_fields = ('description',)  # Поиск по описанию