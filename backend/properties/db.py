import pyodbc

def get_connection():
    return pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=DESKTOP-DL9LPRA;"
        "DATABASE=RealEstate;"
        "Trusted_Connection=yes;"
    )