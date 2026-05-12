from django.shortcuts import render
from django.db import connection

def execute_query(sql_statement, params=None):
    with connection.cursor() as cursor:
        if params:
            cursor.execute(sql_statement, params)
        else:
            cursor.execute(sql_statement)
        
        # convert rows to dictionary
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]

def report_dashboard(request):
    # 1. Most viewed style with max tours
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

    # 2. Property listings with no tours scheduled last month
    q2 = """
    SELECT P.PROPERTY_ID, P.ADDRESS, P.STYLE
    FROM PROPERTY P
    WHERE P.PROPERTY_ID NOT IN (
        SELECT PROPERTY_ID FROM TOUR
        WHERE DATEDIFF(month, TOUR_DATE, GETDATE()) = 1
    )
    """

    # 3. Representative with highest total value of finalized agreements last month
    q3 = """
    SELECT TOP 1
        R.FULL_NAME,
        SUM(A.FINAL_PRICE) AS TOTAL_SALES_VALUE
    FROM AGREEMENT A
    JOIN REPRESENTATIVE R ON A.REPRESENTATIVE_ID = R.REPRESENTATIVE_ID
    WHERE DATEDIFF(month, A.EFFECTIVE_DATE, GETDATE()) = 1
    GROUP BY R.FULL_NAME
    ORDER BY TOTAL_SALES_VALUE DESC
    """

    # 4. Clients who registered last month but have no tours
    q4 = """
    SELECT C.CLIENT_ID, C.FULL_NAME, C.CLIENT_EMAIL
    FROM CLIENT C
    WHERE DATEDIFF(month, C.REGISTRATION_DATE, GETDATE()) = 1
    AND C.CLIENT_ID NOT IN (
        SELECT CLIENT_ID FROM TOUR
    )
    """

    # 5. Available housing units managed by each representative
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

    # 6. Client contact info and total number of attended tours
    q6 = """
    SELECT
        C.FULL_NAME,
        C.CLIENT_PHONE,
        C.CLIENT_EMAIL,
        COUNT(T.TOUR_ID) AS ATTENDED_TOURS
    FROM CLIENT C
    LEFT JOIN TOUR T ON C.CLIENT_ID = T.CLIENT_ID AND T.TOUR_STATUS = 'Completed'
    GROUP BY C.FULL_NAME, C.CLIENT_PHONE, C.CLIENT_EMAIL
    ORDER BY ATTENDED_TOURS DESC
    """

    context = {
        'inquiry1': execute_query(q1),
        'inquiry2': execute_query(q2),
        'inquiry3': execute_query(q3),
        'inquiry4': execute_query(q4),
        'inquiry5': execute_query(q5),
        'inquiry6': execute_query(q6),
    }
    return render(request, 'reports.html', context)