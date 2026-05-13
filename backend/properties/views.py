import json
from django.http import JsonResponse
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render

def add_property_page(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT REPRESENTATIVE_ID, FULL_NAME
            FROM REPRESENTATIVE
            ORDER BY REPRESENTATIVE_ID
        """)
        reps = cursor.fetchall()

    return render(request, "addProperty.html", {
        "reps": reps
    })
def property_page(request):
    return render(request, "property.html")

def list_properties(request):
    with connection.cursor() as cursor:
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
            "market_value": float(row[6]) if row[6] is not None else 0.0,
            "property_status": row[7]
        })
    return JsonResponse(data, safe=False)

@csrf_exempt
def add_property(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            
            # Clean and validate data
            rep_id = data.get("representative_id")
            style = data.get("style")
            lat = data.get("latitude")
            lng = data.get("longitude")
            address = data.get("address")
            market_value = data.get("market_value", "0")
            status = data.get("property_status")

            # Remove commas from market_value if present
            if isinstance(market_value, str):
                market_value = market_value.replace(",", "")
            
            # Convert to float/int where appropriate or use None if empty
            market_value = float(market_value) if market_value else 0
            lat = float(lat) if lat else 0
            lng = float(lng) if lng else 0

            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO PROPERTY
                    (REPRESENTATIVE_ID, STYLE, LATITUDE, LONGITUDE, ADDRESS, MARKET_VALUE, PROPERTY_STATUS)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, [rep_id, style, lat, lng, address, market_value, status])
                
                cursor.execute("SELECT @@IDENTITY")
                new_id = cursor.fetchone()[0]

            return JsonResponse({
                "message": "Property added successfully",
                "property_id": new_id
            })
        except Exception as e:
            return JsonResponse({
                "error": str(e),
                "message": "Error adding property"
            }, status=500)

@csrf_exempt
def update_property(request, property_id):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            
            style = data.get("style")
            address = data.get("address")
            market_value = data.get("market_value", "0")
            status = data.get("property_status")

            # Clean and validate data
            if isinstance(market_value, str):
                market_value = market_value.replace(",", "")
            market_value = float(market_value) if market_value else 0

            with connection.cursor() as cursor:
                cursor.execute("""
                    UPDATE PROPERTY
                    SET STYLE=%s,
                        ADDRESS=%s,
                        MARKET_VALUE=%s,
                        PROPERTY_STATUS=%s
                    WHERE PROPERTY_ID=%s
                """, [style, address, market_value, status, property_id])

            return JsonResponse({"message": "Updated successfully"})
        except Exception as e:
            return JsonResponse({
                "error": str(e),
                "message": "Error updating property"
            }, status=500)

@csrf_exempt
def delete_property(request, property_id):
    if request.method == "DELETE":
        with connection.cursor() as cursor:
            cursor.execute("""
                DELETE FROM PROPERTY
                WHERE PROPERTY_ID=%s
            """, [property_id])

        return JsonResponse({"message": "Deleted successfully"})

def search_properties(request):
    style = request.GET.get("style", "")
    location = request.GET.get("location", "")
    min_price = request.GET.get("min_price", 0)
    max_price = request.GET.get("max_price", 999999999)

    min_price = float(min_price) if min_price else 0.0
    max_price = float(max_price) if max_price else 999999999.0

    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT *
            FROM PROPERTY
            WHERE STYLE LIKE %s
            AND ADDRESS LIKE %s
            AND MARKET_VALUE BETWEEN %s AND %s
        """, [
            f"%{style}%",
            f"%{location}%",
            min_price,
            max_price
        ])
        rows = cursor.fetchall()

    data = []
    for r in rows:
        data.append({
            "property_id": r[0],
            "style": r[2],
            "address": r[5],
            "market_value": float(r[6]) if r[6] is not None else 0.0,
        })

    return JsonResponse(data, safe=False)