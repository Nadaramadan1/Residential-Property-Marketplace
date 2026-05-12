from django.shortcuts import render
from django.db import connection

def execute_query(sql_statement, params=None):
    with connection.cursor() as cursor:
        if params:
            cursor.execute(sql_statement, params)
        else:
            cursor.execute(sql_statement)
        return cursor.fetchall()

def report_dashboard(request):
    q1 = """
    SELECT TOP 1
        P.STYLE,
        COUNT(DISTINCT PV.CLIENT_ID) AS TOTAL_VIEWS,
        COUNT(DISTINCT T.TOUR_ID) AS TOTAL_TOURS
    FROM PROPERTY P
    LEFT JOIN PROPERTY_VIEW PV ON P.PROPERTY_ID = PV.PROPERTY_ID
    LEFT JOIN TOUR T ON P.PROPERTY_ID = T.PROPERTY_ID
    GROUP BY P.STYLE
    ORDER BY TOTAL_TOURS DESC, TOTAL_VIEWS DESC
    """

    q2 = """
    SELECT P.PROPERTY_ID, P.ADDRESS, P.STYLE
    FROM PROPERTY P
    WHERE P.PROPERTY_ID NOT IN (
        SELECT PROPERTY_ID FROM TOUR
        WHERE MONTH(TOUR_DATE) = MONTH(GETDATE()) - 1
    )
    """

    q3 = """
    SELECT TOP 1
        R.FULL_NAME,
        SUM(T.TRANSACTION_AMOUNT) AS TOTAL_SALES
    FROM TRANSACTIONS T
    JOIN REPRESENTATIVE R ON T.REPRESENTATIVE_ID = R.REPRESENTATIVE_ID
    WHERE T.TRANSACTION_STATUS = 'Completed'
    AND MONTH(T.TRANSACTION_DATE) = MONTH(GETDATE()) - 1
    GROUP BY R.FULL_NAME
    ORDER BY TOTAL_SALES DESC
    """

    q4 = """
    SELECT C.CLIENT_ID, C.FULL_NAME, C.CLIENT_EMAIL
    FROM CLIENT C
    WHERE C.CLIENT_ID NOT IN (
        SELECT CLIENT_ID FROM TOUR
        WHERE MONTH(TOUR_DATE) = MONTH(GETDATE()) - 1
    )
    """

    q5 = """
    SELECT
        R.FULL_NAME AS REP_NAME,
        P.PROPERTY_ID,
        P.ADDRESS,
        P.STYLE,
        P.MARKET_VALUE
    FROM PROPERTY P
    JOIN REPRESENTATIVE R ON P.REPRESENTATIVE_ID = R.REPRESENTATIVE_ID
    WHERE P.PROPERTY_STATUS = 'Available'
    ORDER BY R.FULL_NAME
    """

    q6 = """
    SELECT
        C.FULL_NAME,
        C.CLIENT_PHONE,
        C.CLIENT_EMAIL,
        COUNT(T.TOUR_ID) AS TOTAL_TOURS
    FROM CLIENT C
    LEFT JOIN TOUR T ON C.CLIENT_ID = T.CLIENT_ID
    GROUP BY C.FULL_NAME, C.CLIENT_PHONE, C.CLIENT_EMAIL
    """

    context = {
        'inquiry1': execute_query(q1),
        'inquiry2': execute_query(q2),
        'inquiry3': execute_query(q3),
        'inquiry4': execute_query(q4),
        'inquiry5': execute_query(q5),
        'inquiry6': execute_query(q6),
    }
    return render(request, 'reports/dashboard.html', context)