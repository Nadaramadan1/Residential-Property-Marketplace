import json
from django.http import JsonResponse
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render

# ===================== PAGES (HTML) =====================

def agreement_page(request):

    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT a.AGREE_ID,  c.FULL_NAME,  p.ADDRESS,  p.STYLE,
                   a.FINAL_PRICE, CONVERT(VARCHAR, a.EFFECTIVE_DATE, 23)
            FROM AGREEMENT a JOIN CLIENT c ON a.CLIENT_ID = c.CLIENT_ID
            JOIN PROPERTY p ON a.PROPERTY_ID = p.PROPERTY_ID
            ORDER BY a.EFFECTIVE_DATE DESC
        """)

        agreements = cursor.fetchall()

    return render(request, "agreement_list.html", {
        "agreements": agreements
    })

def add_agreement_page(request):
    
    return render(request, "add_agreement.html")

# ===================== AGREEMENTS APIs =====================

def list_agreements(request):
   
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT a.AGREE_ID,
                   a.CLIENT_ID, c.FULL_NAME as CLIENT_NAME,
                   a.PROPERTY_ID, p.ADDRESS, p.STYLE, p.PROPERTY_STATUS,
                   a.FINAL_PRICE,
                   CONVERT(VARCHAR, a.EFFECTIVE_DATE, 23) as EFFECTIVE_DATE
            FROM AGREEMENT a
            JOIN CLIENT c ON a.CLIENT_ID = c.CLIENT_ID
            JOIN PROPERTY p ON a.PROPERTY_ID = p.PROPERTY_ID
            ORDER BY a.EFFECTIVE_DATE DESC
        """)
        rows = cursor.fetchall()

    data = []
    for row in rows:
        data.append({
            "agree_id": row[0],
            "client_id": row[1],
            "client_name": row[2],
            "property_id": row[3],
            "property_address": row[4],
            "property_style": row[5],
            "property_status": row[6],
            "final_price": float(row[7]) if row[7] else None,
            "effective_date": row[8]
        })
    return JsonResponse(data, safe=False)


@csrf_exempt
def add_agreement(request):

    if request.method == "POST":
        data = json.loads(request.body)

        property_id = data.get("property_id")

        with connection.cursor() as cursor:

            cursor.execute("""
                INSERT INTO AGREEMENT
                (CLIENT_ID, PROPERTY_ID, FINAL_PRICE, EFFECTIVE_DATE)
                VALUES (%s, %s, %s, %s)
            """, [
                data.get("client_id"),
                property_id,
                data.get("final_price"),
                data.get("effective_date")
            ])

            cursor.execute("SELECT @@IDENTITY")
            new_id = cursor.fetchone()[0]

            cursor.execute("""
                UPDATE PROPERTY
                SET PROPERTY_STATUS = 'Sold'
                WHERE PROPERTY_ID = %s
            """, [property_id])

        return JsonResponse({
            "message": "Agreement added successfully",
            "agree_id": new_id
        })

    return JsonResponse({"error": "Invalid request"}, status=400)