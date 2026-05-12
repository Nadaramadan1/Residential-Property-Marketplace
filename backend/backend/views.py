from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

def home(request):
    return render(request, 'home.html')

def admin_dashboard(request):
    return render(request, 'adminDashboard.html')

def legal_agreement(request):
    return render(request, 'legalAgreement.html')

def property_details(request):
    return render(request, 'propertyDetails.html')

def property_listing(request):
    return render(request, 'propertyListing.html')

def property_manager(request):
    return render(request, 'propertyManager.html')

def reports(request):
    return render(request, 'reports.html')

def start(request):
    return render(request, 'start.html')

def tour_scheduling(request):
    return render(request, 'tourScheduling.html')

def user_rep_profile(request):
    return render(request, 'user_rep_profile.html')

from django.db import connection
from django.http import JsonResponse
import time
import logging

logger = logging.getLogger(__name__)

def database_health_check(request):
    results = {
        "status": "unknown",
        "connection": False,
        "database_name": "unknown",
        "tables": {},
        "insert_test": "pending",
        "execution_time_ms": 0,
        "errors": []
    }
    
    start_time = time.time()
    
    tables_to_check = [
        "REPRESENTATIVE",
        "CLIENT",
        "PROPERTY",
        "TOUR",
        "AGREEMENT",
        "TRANSACTIONS",
        "PROPERTY_VIEW",
        "IS_FOR"
    ]
    
    try:
        with connection.cursor() as cursor:
            # 1 & 2. Connection and DB Name
            cursor.execute("SELECT DB_NAME()")
            db_name = cursor.fetchone()[0]
            results["connection"] = True
            results["database_name"] = db_name
            
            # 3 & 4. Table existence, Row counts, Sample data
            for table in tables_to_check:
                table_info = {
                    "exists": False,
                    "row_count": 0,
                    "sample_data": []
                }
                try:
                    cursor.execute(f"SELECT COUNT(*) FROM {table}")
                    table_info["row_count"] = cursor.fetchone()[0]
                    table_info["exists"] = True
                    
                    cursor.execute(f"SELECT TOP 5 * FROM {table}")
                    columns = [col[0] for col in cursor.description]
                    rows = cursor.fetchall()
                    table_info["sample_data"] = [dict(zip(columns, row)) for row in rows]
                except Exception as e:
                    logger.error(f"Error accessing table {table}: {e}")
                    results["errors"].append(f"Table {table}: {str(e)}")
                
                results["tables"][table] = table_info
            
            # 5. Insert test (into PROPERTY)
            # We use a transaction to safely rollback the insert test
            try:
                cursor.execute("BEGIN TRAN")
                
                # NOTE: You must adjust the columns and values here based on the exact schema 
                # of the PROPERTY table. This is a generic placeholder test.
                test_id = -99999
                try:
                    # Attempt a generic insert. This will likely fail due to schema constraints (e.g. missing NOT NULL fields).
                    # Update this query with valid test data for your specific schema.
                    cursor.execute("INSERT INTO PROPERTY (PropertyID) VALUES (%s)", [test_id])
                    
                    # Read it back
                    cursor.execute("SELECT * FROM PROPERTY WHERE PropertyID = %s", [test_id])
                    inserted_row = cursor.fetchone()
                    
                    if inserted_row:
                        results["insert_test"] = "Success: Row inserted and read back."
                    else:
                        results["insert_test"] = "Failed: Row not found after insert."
                        
                except Exception as inner_e:
                    results["insert_test"] = f"Failed (Schema constraint/mismatch likely, please update the query in views.py): {str(inner_e)}"
                
                # Clean up / Rollback
                cursor.execute("ROLLBACK TRAN")
                
            except Exception as e:
                error_msg = str(e)
                logger.error(f"Insert test transaction failed: {error_msg}")
                results["insert_test"] = f"Failed: {error_msg}"
                results["errors"].append(f"Insert test error: {error_msg}")

    except Exception as e:
        results["errors"].append(str(e))
        
    end_time = time.time()
    execution_time_ms = round((end_time - start_time) * 1000, 2)
    results["execution_time_ms"] = execution_time_ms
    
    if results["connection"] and not results["errors"]:
        results["status"] = "healthy"
    else:
        results["status"] = "degraded" if results["connection"] else "unhealthy"

    return JsonResponse(results, json_dumps_params={'indent': 4})
