*bd_backup* - содержит бэкап для бд в PostgreSQL  
Примеры команд для проверки *JSON*:  
-http://127.0.0.1:8000/api/customers/
-http://127.0.0.1:8000/api/reservations/  
Примеры с фильтрами:  
-http://127.0.0.1:8000//api/customers/?name=Дмитрий
-http://127.0.0.1:8000//api/customers/?email=petr@gmail.com  
Фильтры работают для полей *name, phone, email* для клиентов  
Для резервирований:* reservation_date, reservation_time, status, customer*
