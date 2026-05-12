# backend/tours/views.py
import json
from django.http import JsonResponse
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect

# ===================== PAGES (HTML) =====================

def tour_page(request):
    """صفحة قائمة الجولات"""
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT t.TOUR_ID, 
                   c.FULL_NAME as CLIENT_NAME,
                   p.ADDRESS, p.STYLE,
                   r.FULL_NAME as REP_NAME,
                   CONVERT(VARCHAR, t.TOUR_DATE, 23) as TOUR_DATE,
                   CONVERT(VARCHAR, t.TOUR_TIME, 108) as TOUR_TIME,
                   t.CLIENT_ID, t.PROPERTY_ID, t.TOUR_STATUS
            FROM TOUR t
            JOIN CLIENT c ON t.CLIENT_ID = c.CLIENT_ID
            JOIN PROPERTY p ON t.PROPERTY_ID = p.PROPERTY_ID
            JOIN REPRESENTATIVE r ON t.REPRESENTATIVE_ID = r.REPRESENTATIVE_ID
            ORDER BY t.TOUR_DATE DESC, t.TOUR_TIME DESC
        """)
        tours = cursor.fetchall()
    return render(request, "tour_list.html", {"tours": tours})

def add_tour_page(request):
    """صفحة إضافة جولة جديدة"""
    if request.method == "POST":
        client_id = request.POST.get("client_id")
        property_id = request.POST.get("property_id")
        representative_id = request.POST.get("representative_id")
        tour_date = request.POST.get("tour_date")
        tour_time = request.POST.get("tour_time")

        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO TOUR (CLIENT_ID, PROPERTY_ID, REPRESENTATIVE_ID, TOUR_DATE, TOUR_TIME, TOUR_STATUS)
                VALUES (%s, %s, %s, %s, %s, 'Scheduled')
            """, [client_id, property_id, representative_id, tour_date, tour_time])
        
        return redirect('tour_page')

    with connection.cursor() as cursor:
        cursor.execute("SELECT CLIENT_ID, FULL_NAME FROM CLIENT")
        clients = cursor.fetchall()
        
        cursor.execute("SELECT PROPERTY_ID, ADDRESS, STYLE, MARKET_VALUE FROM PROPERTY WHERE PROPERTY_STATUS = 'Available'")
        properties = cursor.fetchall()
        
        cursor.execute("SELECT REPRESENTATIVE_ID, FULL_NAME FROM REPRESENTATIVE")
        reps = cursor.fetchall()
        
    return render(request, "add_tour.html", {
        "clients": clients,
        "properties": properties,
        "reps": reps
    })

@csrf_exempt
def update_tour_status(request, tour_id):
    """POST: تحديث حالة الجولة (مثلاً: Completed, No Show, Canceled)"""
    if request.method == "POST":
        data = json.loads(request.body)
        status = data.get("status")

        with connection.cursor() as cursor:
            cursor.execute("""
                UPDATE TOUR SET TOUR_STATUS = %s
                WHERE TOUR_ID = %s
            """, [status, tour_id])

        return JsonResponse({"message": "Tour status updated successfully"})
    return JsonResponse({"error": "Invalid method"}, status=400)

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
    
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM TOUR WHERE TOUR_ID = %s", [tour_id])

    return redirect('tour_page')
