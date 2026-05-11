import json
from .db import get_connection
from django.http import JsonResponse
from django.db import connection
from django.views.decorators.csrf import csrf_exempt

 
def add_property_page(request):
    return render(request, "addproperty.html")

from django.shortcuts import render

def property_page(request):
    return render(request, "property.html")

def list_properties(request):
    cursor = connection.cursor()

    cursor.execute("""
        SELECT PROPERTY_ID, REPRESENTATIVE_ID, STYLE,
               LATITUDE, LONGITUDE, ADDRESS,
               MARKET_VALUE, PROPERTY_STATUS
        FROM PROPERTY
    """)

    rows = cursor.fetchall()

    data = []

    for row in rows:
        data.append({
            "property_id": row[0],
            "representative_id": row[1],
            "style": row[2],
            "latitude": row[3],
            "longitude": row[4],
            "address": row[5],
            "market_value": float(row[6]),
            "property_status": row[7]
        })

    return JsonResponse(data, safe=False)
@csrf_exempt
def add_property(request):
    if request.method == "POST":
        data = json.loads(request.body)

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO PROPERTY
            (REPRESENTATIVE_ID, STYLE, LATITUDE, LONGITUDE, ADDRESS, MARKET_VALUE, PROPERTY_STATUS)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            data["representative_id"],
            data["style"],
            data["latitude"],
            data["longitude"],
            data["address"],
            data["market_value"],
            data["property_status"]
        ))

        cursor.execute("SELECT @@IDENTITY")
        new_id = cursor.fetchone()[0]

        conn.commit()
        conn.close()

        return JsonResponse({
            "message": "Property added successfully",
            "property_id": new_id
        })

@csrf_exempt
def update_property(request, property_id):
    if request.method == "POST":   # هنستخدم POST بدل PUT عشان نتجنب مشاكل
        data = json.loads(request.body)

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE PROPERTY
            SET STYLE=?,
                ADDRESS=?,
                MARKET_VALUE=?,
                PROPERTY_STATUS=?
            WHERE PROPERTY_ID=?
        """, (
            data["style"],
            data["address"],
            data["market_value"],
            data["property_status"],
            property_id
        ))

        conn.commit()
        conn.close()

        return JsonResponse({"message": "Updated successfully"})
@csrf_exempt
def delete_property(request, property_id):
    if request.method == "DELETE":
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            DELETE FROM PROPERTY
            WHERE PROPERTY_ID=?
        """, (property_id,))

        conn.commit()
        conn.close()

        return JsonResponse({"message": "Deleted successfully"})
def search_properties(request):
    style = request.GET.get("style", "")
    location = request.GET.get("location", "")

    min_price = request.GET.get("min_price")
    max_price = request.GET.get("max_price")

    if not min_price:
        min_price = 0
    if not max_price:
        max_price = 999999999

    min_price = float(min_price)
    max_price = float(max_price)

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM PROPERTY
        WHERE STYLE LIKE ?
        AND ADDRESS LIKE ?
        AND MARKET_VALUE BETWEEN ? AND ?
    """, (
        f"%{style}%",
        f"%{location}%",
        min_price,
        max_price
    ))

    rows = cursor.fetchall()

    data = []
    for r in rows:
        data.append({
            "property_id": r[0],
            "style": r[2],
            "address": r[5],
            "market_value": float(r[6]),
        })

    conn.close()
    return JsonResponse(data, safe=False)