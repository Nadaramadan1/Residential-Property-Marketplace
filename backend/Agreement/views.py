import json
from django.http import JsonResponse
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect

# ===================== PAGES (HTML) =====================

def agreement_page(request):
    """صفحة قائمة الاتفاقيات"""
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT a.AGREE_ID,
                   c.FULL_NAME as CLIENT_NAME,
                   p.ADDRESS, p.STYLE,
                   a.FINAL_PRICE,
                   CONVERT(VARCHAR, a.EFFECTIVE_DATE, 23) as EFFECTIVE_DATE
            FROM AGREEMENT a
            JOIN CLIENT c ON a.CLIENT_ID = c.CLIENT_ID
            JOIN PROPERTY p ON a.PROPERTY_ID = p.PROPERTY_ID
            ORDER BY a.EFFECTIVE_DATE DESC
        """)
        agreements = cursor.fetchall()
    return render(request, "agreement_list.html", {"agreements": agreements})

def add_agreement_page(request):
    """صفحة إضافة اتفاقية جديدة"""
    if request.method == "POST":
        client_id = request.POST.get("client_id")
        property_id = request.POST.get("property_id")
        final_price = request.POST.get("final_price")
        effective_date = request.POST.get("effective_date")

        with connection.cursor() as cursor:
            # 1. إضافة الاتفاقية
            cursor.execute("""
                INSERT INTO AGREEMENT (CLIENT_ID, PROPERTY_ID, FINAL_PRICE, EFFECTIVE_DATE)
                VALUES (%s, %s, %s, %s)
            """, [client_id, property_id, final_price, effective_date])
            
            # 2. تحديث حالة العقار إلى مباع
            cursor.execute("""
                UPDATE PROPERTY SET PROPERTY_STATUS = 'Sold'
                WHERE PROPERTY_ID = %s
            """, [property_id])

            # 3. تسجيل المعاملة المالية تلقائياً
            # نأخذ هوية المندوب من العقار
            cursor.execute("SELECT REPRESENTATIVE_ID FROM PROPERTY WHERE PROPERTY_ID = %s", [property_id])
            rep_id = cursor.fetchone()[0]

            cursor.execute("""
                INSERT INTO TRANSACTIONS (CLIENT_ID, REPRESENTATIVE_ID, TRANSACTION_AMOUNT, TRANSACTION_STATUS, TRANSACTION_DATE)
                VALUES (%s, %s, %s, 'Completed', %s)
            """, [client_id, rep_id, final_price, effective_date])
        
        return redirect('agreement_page')

    # Get data for the form
    with connection.cursor() as cursor:
        cursor.execute("SELECT CLIENT_ID, FULL_NAME FROM CLIENT")
        clients = cursor.fetchall()
        
        # We might want to show the current property even if it's 'Reserved' if we are coming from a tour
        cursor.execute("SELECT PROPERTY_ID, ADDRESS, STYLE, MARKET_VALUE FROM PROPERTY WHERE PROPERTY_STATUS IN ('Available', 'Reserved')")
        properties = cursor.fetchall()
        
    # Check for pre-filled data
    pre_client = request.GET.get('client_id')
    pre_prop = request.GET.get('property_id')

    return render(request, "add_agreement.html", {
        "clients": clients,
        "properties": properties,
        "pre_client": pre_client,
        "pre_prop": pre_prop
    })

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
        client_id = data.get("client_id")
        final_price = data.get("final_price")
        effective_date = data.get("effective_date")

        with connection.cursor() as cursor:
            # 1. إضافة الاتفاقية
            cursor.execute("""
                INSERT INTO AGREEMENT (CLIENT_ID, PROPERTY_ID, FINAL_PRICE, EFFECTIVE_DATE)
                VALUES (%s, %s, %s, %s)
            """, [client_id, property_id, final_price, effective_date])
            
            cursor.execute("SELECT @@IDENTITY")
            new_id = cursor.fetchone()[0]

            # 2. تحديث حالة العقار إلى مباع
            cursor.execute("""
                UPDATE PROPERTY SET PROPERTY_STATUS = 'Sold'
                WHERE PROPERTY_ID = %s
            """, [property_id])

            # 3. تسجيل المعاملة المالية تلقائياً
            cursor.execute("SELECT REPRESENTATIVE_ID FROM PROPERTY WHERE PROPERTY_ID = %s", [property_id])
            rep_id = cursor.fetchone()[0]

            cursor.execute("""
                INSERT INTO TRANSACTIONS (CLIENT_ID, REPRESENTATIVE_ID, TRANSACTION_AMOUNT, TRANSACTION_STATUS, TRANSACTION_DATE)
                VALUES (%s, %s, %s, 'Completed', %s)
            """, [client_id, rep_id, final_price, effective_date])

        return JsonResponse({
            "message": "Agreement and Transaction recorded successfully. Property marked as Sold.",
            "agree_id": new_id
        })