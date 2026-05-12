import os
import django
from django.db import connection

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

def populate_test_data():
    with connection.cursor() as cursor:
        # Set some registration dates to last month
        cursor.execute("UPDATE CLIENT SET REGISTRATION_DATE = DATEADD(month, -1, GETDATE()) WHERE CLIENT_ID % 5 = 0")
        
        # Set some tour statuses to 'Completed'
        cursor.execute("UPDATE TOUR SET TOUR_STATUS = 'Completed' WHERE TOUR_ID % 2 = 0")
        
        # Set some agreement dates to last month
        cursor.execute("UPDATE AGREEMENT SET EFFECTIVE_DATE = DATEADD(month, -1, GETDATE()) WHERE AGREE_ID % 3 = 0")
        
        # Set some tours to last month
        cursor.execute("UPDATE TOUR SET TOUR_DATE = DATEADD(month, -1, GETDATE()) WHERE TOUR_ID % 4 = 0")
        
        print("Test data updated successfully.")

if __name__ == "__main__":
    populate_test_data()
