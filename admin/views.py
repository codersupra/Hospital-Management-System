from django.shortcuts import render
from users.models import Doctors, Patients

def admin_dashboard(request):
    total_doctors = Doctors.objects.count()
    total_patients = Patients.objects.count()
    context = {
        'total_doctors': total_doctors,
        'total_patients': total_patients,
    }
    return render(request, 'admin/dashboard.html')
