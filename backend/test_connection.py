import pyodbc

def get_db_connection():
    try:
        conn = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER=DESKTOP-MEKUU7J;' 
            'DATABASE=RealEstate;'      
            'Trusted_Connection=yes;'             
        )
        return conn
    except Exception as e:
        print(f"connection failed {e}")
        return None

def execute_query(sql_statement, params=None, is_select=True):
    connection = get_db_connection()
    if not connection:
        return None
    
    cursor = connection.cursor()
    try:
        if params:
            cursor.execute(sql_statement, params)
        else:
            cursor.execute(sql_statement)
            
        if is_select:
            columns = [column[0] for column in cursor.description]
            results = [dict(zip(columns, row)) for row in cursor.fetchall()]
            return results
        else:
            connection.commit()
            return True
    except Exception as e:
        print(f"wrong in query execution: {e}")
        return None
    finally:
        connection.close()

if __name__ == "__main__":
    print("Testing connection...")
    res = execute_query("SELECT 1 as test")
    if res:
        print("Success! Connection established and query executed.")
        print(f"Result: {res}")
    else:
        print("Failed to connect or execute query.")