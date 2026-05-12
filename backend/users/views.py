import json
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.db import connection
from django.views.decorators.csrf import csrf_exempt

# --- 1. PAGE RENDERING VIEWS (قوالب العرض) ---

def view_home(request):
    return render(request, "home.html")

def clients_list_page(request):
    with connection.cursor() as cursor:
        # متوافق مع جدول CLIENT
        cursor.execute("""
            SELECT CLIENT_ID, FULL_NAME, CLIENT_CONTACT_PREFERENCE, 
                   CLIENT_PHONE, CLIENT_EMAIL 
            FROM CLIENT
            ORDER BY CLIENT_ID
        """)
        clients = cursor.fetchall()
    return render(request, "clients_list.html", {"clients": clients})

def add_client_page(request):
    if request.method == "POST":
        name = request.POST.get("name")
        contact_pref = request.POST.get("contact_preference")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO CLIENT (FULL_NAME, CLIENT_CONTACT_PREFERENCE, CLIENT_PHONE, CLIENT_EMAIL, REGISTRATION_DATE)
                VALUES (%s, %s, %s, %s, GETDATE())
            """, [name, contact_pref, phone, email])
        return redirect("clients_list")
    return render(request, "add_client.html")

def update_client_page(request, id):
    with connection.cursor() as cursor:
        if request.method == "POST":
            name = request.POST.get("name")
            contact_pref = request.POST.get("contact_preference")
            phone = request.POST.get("phone")
            email = request.POST.get("email")
            
            cursor.execute("""
                UPDATE CLIENT 
                SET FULL_NAME = %s, CLIENT_CONTACT_PREFERENCE = %s, 
                    CLIENT_PHONE = %s, CLIENT_EMAIL = %s
                WHERE CLIENT_ID = %s
            """, [name, contact_pref, phone, email, id])
            return redirect("clients_list")
        
        cursor.execute("""
            SELECT CLIENT_ID, FULL_NAME, CLIENT_CONTACT_PREFERENCE, 
                   CLIENT_PHONE, CLIENT_EMAIL 
            FROM CLIENT WHERE CLIENT_ID = %s
        """, [id])
        client = cursor.fetchone()
    return render(request, "update_client.html", {"client": client})

def representatives_list_page(request):
    with connection.cursor() as cursor:
        # متوافق مع جدول REPRESENTATIVE
        cursor.execute("""
            SELECT REPRESENTATIVE_ID, FULL_NAME, PHONE, EMAIL, LICENSE_NUMBER 
            FROM REPRESENTATIVE
            ORDER BY REPRESENTATIVE_ID
        """)
        representatives = cursor.fetchall()
    return render(request, "representatives_list.html", {"representatives": representatives})

def add_representative_page(request):
    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        license_num = request.POST.get("license_num")
        
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO REPRESENTATIVE (FULL_NAME, PHONE, EMAIL, LICENSE_NUMBER) 
                VALUES (%s, %s, %s, %s)
            """, [name, phone, email, license_num])
        return redirect("representatives_list")
    return render(request, "add_representative.html")

def update_representative_page(request, id):
    with connection.cursor() as cursor:
        if request.method == "POST":
            name = request.POST.get("name")
            phone = request.POST.get("phone")
            email = request.POST.get("email")
            license_num = request.POST.get("license_num")
            
            cursor.execute("""
                UPDATE REPRESENTATIVE 
                SET FULL_NAME = %s, PHONE = %s, EMAIL = %s, LICENSE_NUMBER = %s
                WHERE REPRESENTATIVE_ID = %s
            """, [name, phone, email, license_num, id])
            return redirect("representatives_list")

        cursor.execute("""
            SELECT REPRESENTATIVE_ID, FULL_NAME, PHONE, EMAIL, LICENSE_NUMBER 
            FROM REPRESENTATIVE WHERE REPRESENTATIVE_ID = %s
        """, [id])
        representative = cursor.fetchone()
    return render(request, "update_representative.html", {"representative": representative})


# --- 2. DELETE ACTIONS (عمليات الحذف) ---

def delete_client(request, id):
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM CLIENT WHERE CLIENT_ID = %s", [id])
    return redirect("clients_list")

def delete_representative(request, id):
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM REPRESENTATIVE WHERE REPRESENTATIVE_ID = %s", [id])
    return redirect("representatives_list")


# --- 3. JSON API VIEWS (للتعامل مع AJAX أو تطبيقات خارجية) ---

def list_clients_api(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT CLIENT_ID, FULL_NAME, CLIENT_CONTACT_PREFERENCE, CLIENT_PHONE, CLIENT_EMAIL FROM CLIENT")
        rows = cursor.fetchall()
    clients = [{"client_id": r[0], "full_name": r[1], "contact_preference": r[2], "phone": r[3], "email": r[4]} for r in rows]
    return JsonResponse(clients, safe=False)

@csrf_exempt
def add_client_api(request):
    if request.method == "POST":
        data = json.loads(request.body)
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO CLIENT (FULL_NAME, CLIENT_CONTACT_PREFERENCE, CLIENT_PHONE, CLIENT_EMAIL, REGISTRATION_DATE)
                VALUES (%s, %s, %s, %s, GETDATE())
            """, [data.get("name"), data.get("contact_preference"), data.get("phone"), data.get("email")])
        return JsonResponse({"message": "Client added successfully!"})
    return JsonResponse({"error": "Invalid method"}, status=400)

def list_representatives_api(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT REPRESENTATIVE_ID, FULL_NAME, PHONE, EMAIL, LICENSE_NUMBER FROM REPRESENTATIVE")
        rows = cursor.fetchall()
    reps = [{"representative_id": r[0], "full_name": r[1], "phone": r[2], "email": r[3], "license_number": r[4]} for r in rows]
    return JsonResponse(reps, safe=False)

@csrf_exempt
def delete_representative_api(request, id):
    if request.method == "DELETE":
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM REPRESENTATIVE WHERE REPRESENTATIVE_ID = %s", [id])
        return JsonResponse({"message": "Representative deleted successfully!"})
    return JsonResponse({"error": "Invalid method"}, status=400)