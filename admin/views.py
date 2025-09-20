from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from users.models import Doctors, Patients, Users, AdminUser, Admins

def admin_dashboard(request):
    # Check if admin is logged in via session
    if not request.session.get('is_admin_logged_in'):
        from django.contrib import messages
        from django.shortcuts import redirect
        messages.error(request, 'Please login to access admin dashboard.')
        return redirect('admin_login')
    
    # Get admin user and admin details from session
    try:
        admin_user_id = request.session.get('admin_user_id')
        
        if not admin_user_id:
            from django.contrib import messages
            from django.shortcuts import redirect
            messages.error(request, 'Invalid session. Please login again.')
            return redirect('admin_login')
            
        admin_user = AdminUser.objects.get(id=admin_user_id)
        admin = Admins.objects.get(user=admin_user)  # Use the OneToOne relationship directly
        
        # Check if admin is still active
        if not admin.is_active or not admin_user.is_active_admin:
            from django.contrib import messages
            from django.shortcuts import redirect
            messages.error(request, 'Your admin privileges are inactive.')
            # Clear session
            request.session.flush()
            return redirect('admin_login')
            
    except (AdminUser.DoesNotExist, Admins.DoesNotExist):
        from django.contrib import messages
        from django.shortcuts import redirect
        messages.error(request, 'Admin record not found. Please login again.')
        # Clear session
        request.session.flush()
        return redirect('admin_login')
    
    # Calculate statistics
    total_doctors = Doctors.objects.count()
    total_patients = Patients.objects.count()
    total_users = Users.objects.count()
    total_admins = AdminUser.objects.count()
    
    # Recent activity (you can expand this)
    recent_doctors = Doctors.objects.select_related('user').order_by('-user__date_joined')[:5]
    recent_patients = Patients.objects.select_related('user').order_by('-user__date_joined')[:5]
    
    context = {
        'admin_user': admin_user,  # Use the retrieved admin_user instead of request.user
        'admin': admin,
        'total_doctors': total_doctors,
        'total_patients': total_patients,
        'total_users': total_users,
        'total_admins': total_admins,
        'recent_doctors': recent_doctors,
        'recent_patients': recent_patients,
    }
    return render(request, 'admins/admin_dashboard.html', context)
