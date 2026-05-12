from django.db import connection
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

def check_columns():
    with connection.cursor() as cursor:
        try:
            cursor.execute("SELECT TOP 0 * FROM PROPERTY")
            columns = [col[0] for col in cursor.description]
            print(f"Columns in PROPERTY: {columns}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    check_columns()
