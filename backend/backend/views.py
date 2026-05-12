from django.shortcuts import render

def add_client_page(request):
    return render(request, 'add_client.html')

def clients_list_page(request):
    return render(request, 'clients_list.html') 


def add_representative_page(request):
    return render(request, 'add_representative.html')

def representatives_list_page(request):
    return render(request, 'representatives_list.html')

def update_representative_page(request, id):
    return render(request, 'update_representative.html')

def update_client_page(request, id):
    return render(request, 'update_client.html')

def delete_client(request, id):
    return render(request, 'delete_client.html')

def delete_representative(request, id):
    return render(request, 'delete_representative.html')


from django.db import connection

def view_home(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM PROPERTY")
        prop_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM CLIENT")
        client_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM REPRESENTATIVE")
        rep_count = cursor.fetchone()[0]
        
    context = {
        'prop_count': prop_count,
        'client_count': client_count,
        'rep_count': rep_count,
    }
    return render(request, 'home.html', context)

def view_dashboard(request):
    return render(request, 'dashboard.html')


