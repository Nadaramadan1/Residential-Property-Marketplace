import pyodbc

conn = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=DESKTOP-Q4QQDN9\\SQLEXPRESS;'
    'DATABASE=PropertyMarketplace;'
    'Trusted_Connection=yes;'
)

cursor = conn.cursor()
cursor.execute("SELECT 1 AS test")
row = cursor.fetchone()
print("✅ Connection successful! Result:", row[0])

conn.close()