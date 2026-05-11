from django.shortcuts import render
from test_connection import execute_query

def report_dashboard(request):
    # Q1 — Most requested property style (by tours)
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

    # Q2 — Properties that had no tours last month
    q2 = """
    SELECT P.PROPERTY_ID, P.ADDRESS, P.STYLE
    FROM PROPERTY P
    WHERE P.PROPERTY_ID NOT IN (
        SELECT PROPERTY_ID FROM TOUR
        WHERE MONTH(TOUR_DATE) = MONTH(GETDATE()) - 1
    )
    """

    # Q3 — Top performing representative last month (by completed sales)
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

    # Q4 — Registered clients with no tours last month
    q4 = """
    SELECT C.CLIENT_ID, C.FULL_NAME, C.CLIENT_EMAIL
    FROM CLIENT C
    WHERE C.CLIENT_ID NOT IN (
        SELECT CLIENT_ID FROM TOUR
        WHERE MONTH(TOUR_DATE) = MONTH(GETDATE()) - 1
    )
    """

    # Q5 — Available properties per representative
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

    # Q6 — All clients with their total tour count
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