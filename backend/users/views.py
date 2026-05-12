from django.shortcuts import render , redirect
from django.db import connection

# Create your views here.
def add_client(request):
    if request.method == "POST":
        name = request.POST.get("name")
        contact_pref = request.POST.get("contact_preference")
        phone = request.POST.get("phone")
        email = request.POST.get("email")

        with connection.cursor() as cursor:
            cursor.execute("""INSERT INTO CLIENT
            (FULL_NAME, CLIENT_CONTACT_PREFERENCE, CLIENT_PHONE, CLIENT_EMAIL)
             VALUES (%s, %s, %s, %s)
            """, [name, contact_pref, phone, email])

        return redirect("clients_list")

    return render(request, "add_client.html")


def clients_list(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT CLIENT_ID, FULL_NAME,CLIENT_CONTACT_PREFERENCE, CLIENT_PHONE, CLIENT_EMAIL FROM CLIENT")
        clients = cursor.fetchall()

    return render(request, "clients_list.html", {"clients": clients})

def add_representative(request):
    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        license_num = request.POST.get("license_num")

        with connection.cursor() as cursor:
            cursor.execute("""INSERT INTO REPRESENTATIVE 
            (FULL_NAME, PHONE, EMAIL, LICENSE_NUMBER) 
            VALUES  (%s, %s, %s, %s)""" , [name, phone, email, license_num])

        return redirect("representatives_list")

    return render(request, "add_representative.html")


def representatives_list(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT REPRESENTATIVE_ID, FULL_NAME, PHONE, EMAIL, LICENSE_NUMBER FROM REPRESENTATIVE")
        representatives = cursor.fetchall()

        return render(request, "representatives_list.html", {"representatives": representatives})

def update_client(request, id):
    with connection.cursor() as cursor:
        cursor.execute(""" SELECT 
        CLIENT_ID ,FULL_NAME, CLIENT_CONTACT_PREFERENCE, CLIENT_PHONE, CLIENT_EMAIL
        FROM CLIENT WHERE CLIENT_ID = %s """, [id] )
        client = cursor.fetchone()

    if request.method == "POST":
        name = request.POST.get("name")
        contact_pref = request.POST.get("contact_preference")
        phone = request.POST.get("phone")
        email = request.POST.get("email")

        with connection.cursor() as cursor:
            cursor.execute(""" UPDATE CLIENT SET FULL_NAME = %s
             , CLIENT_CONTACT_PREFERENCE = %s , CLIENT_PHONE = %s, CLIENT_EMAIL = %s
             WHERE CLIENT_ID = %s""", [name, contact_pref, phone, email, id])

        return redirect("clients_list")

    return render(request, "update_client.html", {"client": client})


def update_representative(request , id):
    with connection.cursor() as cursor:
        cursor.execute(""" SELECT REPRESENTATIVE_ID , FULL_NAME, PHONE, EMAIL, LICENSE_NUMBER 
         FROM REPRESENTATIVE WHERE REPRESENTATIVE_ID = %s """ , [id])
        representative = cursor.fetchone()

    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        license_num = request.POST.get("license_num")

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








