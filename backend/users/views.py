import json
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.db import connection
from django.views.decorators.csrf import csrf_exempt

# --- PAGE RENDERING VIEWS ---

def clients_list_page(request):
    return render(request, "clients_list.html")

def add_client_page(request):
    return render(request, "add_client.html")

def update_client_page(request, id):
    return render(request, "update_client.html", {"client_id": id})

def representatives_list_page(request):
    return render(request, "representatives_list.html")

def add_representative_page(request):
    return render(request, "add_representative.html")

def update_representative_page(request, id):
    return render(request, "update_representative.html", {"representative_id": id})

# --- JSON API VIEWS ---

def list_clients(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT CLIENT_ID, FULL_NAME, CLIENT_CONTACT_PREFERENCE, CLIENT_PHONE, CLIENT_EMAIL FROM CLIENT")
        rows = cursor.fetchall()
        
    clients = []
    for row in rows:
        clients.append({
            "client_id": row[0],
            "full_name": row[1],
            "contact_preference": row[2],
            "phone": row[3],
            "email": row[4]
        })
    return JsonResponse(clients, safe=False)

def get_client(request, id):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT CLIENT_ID, FULL_NAME, CLIENT_CONTACT_PREFERENCE, CLIENT_PHONE, CLIENT_EMAIL 
            FROM CLIENT WHERE CLIENT_ID = %s
        """, [id])
        row = cursor.fetchone()
        
    if not row:
        return JsonResponse({"error": "Client not found"}, status=404)
        
    client = {
        "client_id": row[0],
        "full_name": row[1],
        "contact_preference": row[2],
        "phone": row[3],
        "email": row[4]
    }
    return JsonResponse(client)

@csrf_exempt
def add_client_api(request):
    if request.method == "POST":
        data = json.loads(request.body)
        name = data.get("name")
        contact_pref = data.get("contact_preference")
        phone = data.get("phone")
        email = data.get("email")

        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO CLIENT (FULL_NAME, CLIENT_CONTACT_PREFERENCE, CLIENT_PHONE, CLIENT_EMAIL)
                VALUES (%s, %s, %s, %s)
            """, [name, contact_pref, phone, email])

        return JsonResponse({"message": "Client added successfully!"})
    return JsonResponse({"error": "Invalid method"}, status=400)

@csrf_exempt
def update_client_api(request, id):
    if request.method in ["POST", "PUT"]:
        data = json.loads(request.body)
        name = data.get("name")
        contact_pref = data.get("contact_preference")
        phone = data.get("phone")
        email = data.get("email")

        with connection.cursor() as cursor:
            cursor.execute("""
                UPDATE CLIENT SET FULL_NAME = %s, CLIENT_CONTACT_PREFERENCE = %s, 
                CLIENT_PHONE = %s, CLIENT_EMAIL = %s
                WHERE CLIENT_ID = %s
            """, [name, contact_pref, phone, email, id])

        return JsonResponse({"message": "Client updated successfully!"})
    return JsonResponse({"error": "Invalid method"}, status=400)

@csrf_exempt
def delete_client_api(request, id):
    if request.method == "DELETE":
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM CLIENT WHERE CLIENT_ID = %s", [id])
        return JsonResponse({"message": "Client deleted successfully!"})
    return JsonResponse({"error": "Invalid method"}, status=400)

def list_representatives(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT REPRESENTATIVE_ID, FULL_NAME, PHONE, EMAIL, LICENSE_NUMBER FROM REPRESENTATIVE")
        rows = cursor.fetchall()
        
    reps = []
    for row in rows:
        reps.append({
            "representative_id": row[0],
            "full_name": row[1],
            "phone": row[2],
            "email": row[3],
            "license_number": row[4]
        })
    return JsonResponse(reps, safe=False)

def get_representative(request, id):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT REPRESENTATIVE_ID, FULL_NAME, PHONE, EMAIL, LICENSE_NUMBER 
            FROM REPRESENTATIVE WHERE REPRESENTATIVE_ID = %s
        """, [id])
        row = cursor.fetchone()
        
    if not row:
        return JsonResponse({"error": "Representative not found"}, status=404)
        
    rep = {
        "representative_id": row[0],
        "full_name": row[1],
        "phone": row[2],
        "email": row[3],
        "license_number": row[4]
    }
    return JsonResponse(rep)

@csrf_exempt
def add_representative_api(request):
    if request.method == "POST":
        data = json.loads(request.body)
        name = data.get("name")
        phone = data.get("phone")
        email = data.get("email")
        license_num = data.get("license_num")

        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO REPRESENTATIVE (FULL_NAME, PHONE, EMAIL, LICENSE_NUMBER) 
                VALUES (%s, %s, %s, %s)
            """, [name, phone, email, license_num])

        return JsonResponse({"message": "Representative added successfully!"})
    return JsonResponse({"error": "Invalid method"}, status=400)

@csrf_exempt
def update_representative_api(request, id):
    if request.method in ["POST", "PUT"]:
        data = json.loads(request.body)
        name = data.get("name")
        phone = data.get("phone")
        email = data.get("email")
        license_num = data.get("license_num")

        with connection.cursor() as cursor:
            cursor.execute(""" UPDATE REPRESENTATIVE SET FULL_NAME = %s , PHONE = %s, EMAIL = %s, LICENSE_NUMBER = %s
            WHERE REPRESENTATIVE_ID = %s """, [name, phone, email, license_num, id])

        return redirect("representatives_list")

    return render(request, "update_representative.html", {"representative": representative})


def delete_client(request, id):
    with connection.cursor() as cursor:
        cursor.execute(""" DELETE FROM CLIENT WHERE CLIENT_ID = %s """, [id])
        return redirect("clients_list")

def delete_representative(request, id):
    with connection.cursor() as cursor:
        cursor.execute(""" DELETE FROM REPRESENTATIVE WHERE REPRESENTATIVE_ID = %s """, [id])
        return redirect("representatives_list")

def view_home(request):
    return render(request, "home.html")







    return JsonResponse({"message": "Representative updated successfully!"})
    return JsonResponse({"error": "Invalid method"}, status=400)

@csrf_exempt
def delete_representative_api(request, id):
    if request.method == "DELETE":
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM REPRESENTATIVE WHERE REPRESENTATIVE_ID = %s", [id])
        return JsonResponse({"message": "Representative deleted successfully!"})
    return JsonResponse({"error": "Invalid method"}, status=400)
