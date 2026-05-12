# backend/tours/views.py
import json
from django.http import JsonResponse
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render

# ===================== PAGES (HTML) =====================

def tour_page(request):
    """صفحة قائمة الجولات"""
    return render(request, "tours/tour_list.html")

def add_tour_page(request):
    """صفحة إضافة جولة جديدة"""
    return render(request, "tours/add_tour.html")

# ===================== TOURS APIs =====================

def list_tours(request):
    """GET: جلب جميع الجولات مع بيانات العميل والعقار والموظف"""
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT t.TOUR_ID, 
                   t.CLIENT_ID, c.FULL_NAME as CLIENT_NAME,
                   t.PROPERTY_ID, p.ADDRESS, p.STYLE,
                   t.REPRESENTATIVE_ID, r.FULL_NAME as REP_NAME,
                   CONVERT(VARCHAR, t.TOUR_DATE, 23) as TOUR_DATE,
                   CONVERT(VARCHAR, t.TOUR_TIME, 108) as TOUR_TIME
            FROM TOUR t
            JOIN CLIENT c ON t.CLIENT_ID = c.CLIENT_ID
            JOIN PROPERTY p ON t.PROPERTY_ID = p.PROPERTY_ID
            JOIN REPRESENTATIVE r ON t.REPRESENTATIVE_ID = r.REPRESENTATIVE_ID
            ORDER BY t.TOUR_DATE DESC, t.TOUR_TIME DESC
        """)
        rows = cursor.fetchall()

    data = []
    for row in rows:
        data.append({
            "tour_id": row[0],
            "client_id": row[1],
            "client_name": row[2],
            "property_id": row[3],
            "property_address": row[4],
            "property_style": row[5],
            "representative_id": row[6],
            "representative_name": row[7],
            "tour_date": row[8],
            "tour_time": row[9]
        })
    return JsonResponse(data, safe=False)


@csrf_exempt
def add_tour(request):
    """POST: إضافة جولة جديدة"""
    if request.method == "POST":
        data = json.loads(request.body)

        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO TOUR (CLIENT_ID, PROPERTY_ID, REPRESENTATIVE_ID, TOUR_DATE, TOUR_TIME)
                VALUES (%s, %s, %s, %s, %s)
            """, [
                data.get("client_id"),
                data.get("property_id"),
                data.get("representative_id"),
                data.get("tour_date"),
                data.get("tour_time")
            ])
            cursor.execute("SELECT @@IDENTITY")
            new_id = cursor.fetchone()[0]

        return JsonResponse({
            "message": "Tour added successfully",
            "tour_id": new_id
        })


@csrf_exempt
def delete_tour(request, tour_id):
    
    if request.method == "DELETE":
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM TOUR WHERE TOUR_ID = %s", [tour_id])

        return JsonResponse({"message": "Tour deleted successfully"})
