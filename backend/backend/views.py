from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

def home(request):
    return render(request, 'home.html')

def admin_dashboard(request):
    return render(request, 'adminDashboard.html')

def legal_agreement(request):
    return render(request, 'legalAgreement.html')

def property_details(request):
    return render(request, 'propertyDetails.html')

def property_listing(request):
    return render(request, 'propertyListing.html')

def property_manager(request):
    return render(request, 'propertyManager.html')

def reports(request):
    return render(request, 'reports.html')

def start(request):
    return render(request, 'start.html')

def tour_scheduling(request):
    return render(request, 'tourScheduling.html')

def user_rep_profile(request):
    return render(request, 'user_rep_profile.html')