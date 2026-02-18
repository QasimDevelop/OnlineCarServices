import os
import django
from django.db import connection
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "car_services_backend.settings")
django.setup()

with connection.cursor() as cursor:
    cursor.execute(" SELECT * from ServiceType ")
    print(cursor.fetchall())
    