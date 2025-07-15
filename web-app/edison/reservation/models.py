from django.db import models


class Actions(models.Model):
    ACTION_CHOICES = [
        ('Подтверждение', 'Подтверждение'),
        ('Отмена', 'Отмена'),
        ('Перенос', 'Перенос'),
    ]
    id = models.AutoField(primary_key=True, verbose_name="ID")
    reservation_number = models.ForeignKey('Reservations', on_delete=models.CASCADE, db_column='reservation_number', verbose_name="Номер брони")
    administrator = models.ForeignKey('Administrators', on_delete=models.CASCADE, verbose_name='Администраторы')
    performed_action = models.CharField(max_length=50, choices=ACTION_CHOICES, verbose_name='Выполненное действие')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Время создания записи')

    def __str__(self):
        return f"{self.administrator.name} - {self.performed_action} - {self.reservation_number}"

    class Meta:
        managed = False
        db_table = 'actions'
        verbose_name = 'Действие'
        verbose_name_plural = 'Действия'


class Administrators(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='ID')
    login = models.CharField(max_length=255, verbose_name='Логин')
    name = models.CharField(max_length=255, verbose_name='ФИО')
    phone = models.CharField(max_length=12, verbose_name='Номер телефона')
    email = models.CharField(max_length=255, verbose_name='Электронная почта')

    def __str__(self):
        return f"{self.login} - {self.name}"

    class Meta:
        managed = False
        db_table = 'administrators'
        verbose_name = 'Администратор'
        verbose_name_plural = 'Администраторы'


class Customers(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='ID')
    name = models.CharField(max_length=255, verbose_name='ФИО')
    phone = models.CharField(max_length=12, verbose_name='Номер телефона')
    email = models.CharField(max_length=255, verbose_name='Электронная почта', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Время создания записи')
    staff_comment = models.CharField(max_length=255, verbose_name='Комментарии персонала', null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = 'customers'
        verbose_name = 'Посетитель'
        verbose_name_plural = 'Посетители'


class Reservations(models.Model):
    STATUS_CHOICES = [
        ('В ожидании подтверждения', 'В ожидании подтверждения' ),
        ('Подтверждено', 'Подтверждено'),
        ('Отменено', 'Отменено'),
    ]

    reservation_number = models.AutoField(primary_key=True, verbose_name='Номер резервирования')
    table_number = models.ForeignKey('Tables', on_delete=models.CASCADE, db_column='table_number', verbose_name='Номер стола', null=True, blank=True)
    customer = models.ForeignKey(Customers, on_delete=models.CASCADE, verbose_name='Клиент')
    reservation_date = models.DateField(verbose_name='Дата резервирования')
    reservation_time = models.TimeField(verbose_name='Время резервирования')
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending', verbose_name='Статус бронирования')
    customer_count =  models.IntegerField(verbose_name='Количество посетителей')
    comments = models.CharField(max_length=255, verbose_name='Пожелания', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Время создания записи')

    def __str__(self):
        return f"Бронь {self.reservation_number} - {self.customer.name} - {self.reservation_date} {self.reservation_time} - {self.status}"

    class Meta:
        managed = False
        db_table = 'reservations'
        verbose_name = 'Резервирование'
        verbose_name_plural = 'Резервирования'


class Tables(models.Model):
    number = models.AutoField(primary_key=True, verbose_name='Номер стола')
    capacity = models.IntegerField(verbose_name='Вместительность')
    description = models.CharField(max_length=255, blank=True, null=True, verbose_name='Описание')

    def __str__(self):
        return f"Столик {self.number} ({self.capacity} чел.) - {self.description}"

    class Meta:
        managed = False
        db_table = 'tables'
        verbose_name = 'Место'
        verbose_name_plural = 'Места'