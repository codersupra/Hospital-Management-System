from django.shortcuts import render

from multiprocessing import context
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
from .models import *
from .helpers import send_email
import uuid


Users = get_user_model()

def register_admin(request):
    if request.method == 'POST':
        # Get form data
        hospital_name = request.POST.get('hospital_name')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('conf_password')
        employee_id = request.POST.get('employee_id')
        department = request.POST.get('department')
        hire_date = request.POST.get('hire_date')
        phone = request.POST.get('phone')
        role = request.POST.get('role')
        access_level = request.POST.get('access_level')
        
        # Address fields
        address_line = request.POST.get('address_line')
        region = request.POST.get('region')
        city = request.POST.get('city')
        pincode = request.POST.get('pincode')

        profile_pic = ""
        if "profile_pic" in request.FILES:
            profile_pic = request.FILES['profile_pic']

        # Form context for re-rendering on error
        form_context = {
            'hospital_name': hospital_name, 'first_name': first_name, 'last_name': last_name,
            'username': username, 'email': email, 'employee_id': employee_id,
            'department': department, 'hire_date': hire_date, 'phone': phone,
            'role': role, 'access_level': access_level, 'address_line': address_line,
            'region': region, 'city': city, 'pincode': pincode
        }

        # Validation
        if len(password) < 6:
            messages.error(request, 'Password must be at least 6 characters long.')
            return render(request, 'users/register_admin.html', context=form_context)

        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'users/register_admin.html', context=form_context)

        # Check if username or email already exists
        if AdminUser.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists. Please choose a different username.')
            return render(request, 'users/register_admin.html', context=form_context)

        if AdminUser.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists. Please use a different email.')
            return render(request, 'users/register_admin.html', context=form_context)

        if AdminUser.objects.filter(employee_id=employee_id).exists():
            messages.error(request, 'Employee ID already exists. Please use a different employee ID.')
            return render(request, 'users/register_admin.html', context=form_context)

        try:
            # Create address if provided
            address = None
            if address_line and city:
                address = Address.objects.create(
                    address_line=address_line,
                    region=region or '',
                    city=city,
                    code_postal=pincode or ''
                )

            # Create AdminUser
            admin_user = AdminUser.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                hospital_name=hospital_name,
                employee_id=employee_id,
                department=department,
                hire_date=hire_date,
                phone=phone or '',
                profile_avatar=profile_pic,
                address=address,
                is_active_admin=True
            )

            # Create corresponding Admins entry
            admin = Admins.objects.create(
                user=admin_user,
                role=role,
                access_level=access_level or 'read',
                is_active=True
            )

            messages.success(request, 'Admin account has been successfully registered! Please login.')
            return redirect('admin_login')

        except Exception as e:
            messages.error(request, f'An error occurred during registration: {str(e)}')
            return render(request, 'users/register_admin.html', context=form_context)

    # GET request - show empty form
    return render(request, 'users/register_admin.html')

def register(request):
  specialities = Specialty.objects.all()
  if request.method == 'POST':
    user_status = request.POST.get('user_config')
    first_name = request.POST.get('user_firstname')
    last_name = request.POST.get('user_lastname')
    profile_pic = ""

    if "profile_pic" in request.FILES:
      profile_pic = request.FILES['profile_pic']

    username = request.POST.get('user_id')
    email = request.POST.get('email')
    gender = request.POST.get('user_gender')
    birthday = request.POST.get("birthday")
    password = request.POST.get('password')
    confirm_password = request.POST.get('conf_password')
    address_line = request.POST.get('address_line')
    region = request.POST.get('region')
    city = request.POST.get('city')
    pincode = request.POST.get('pincode')

    if len(password) < 6:
      messages.error(request, 'Password must be at least 6 characters long.')
      return render(request, 'users/register.html', context={'user_config': user_status, 'user_firstname': first_name, 'user_lastname': last_name, 'user_id': username, 'email': email, 'user_gender': gender, 'address_line': address_line, 'region': region, 'city': city, 'pincode': pincode, 'specialities': specialities})

    if password != confirm_password:
      messages.error(request, 'Passwords do not match.')
      return render(request, 'users/register.html', context={'user_config': user_status, 'user_firstname': first_name, 'user_lastname': last_name, 'user_id': username, 'email': email, 'user_gender': gender, 'address_line': address_line, 'region': region, 'city': city, 'pincode': pincode, 'specialities': specialities})

    if Users.objects.filter(username=username).exists():
      messages.error(request, 'Username already exists. Try again with a different username.')
      return render(request, 'users/register.html', context={'user_config': user_status, 'user_firstname': first_name, 'user_lastname': last_name, 'user_id': username, 'email': email, 'user_gender': gender, 'address_line': address_line, 'region': region, 'city': city, 'pincode': pincode, 'specialities': specialities})

    address = Address.objects.create(address_line=address_line, region=region,city=city, code_postal=pincode)

    user = Users.objects.create_user(
      first_name=first_name,
      last_name=last_name,
      profile_avatar=profile_pic,
      username=username,
      email=email,
      gender=gender,
      birthday=birthday,
      password=password,
      id_address=address,
      is_doctor=(user_status == 'Doctor')
    )
      
    user.save()

    if user_status == 'Doctor':
      specialty = request.POST.get('Speciality')
      specialty_name = Specialty.objects.get(name=specialty)
      bio = request.POST.get('bio')
      doctor = Doctors.objects.create(user=user, specialty=specialty_name, bio=bio)
      doctor.save()
        
    elif user_status == 'Patient':
        insurance = request.POST.get('insurance')
        patient = Patients.objects.create(user=user, insurance=insurance)
        patient.save()

    messages.success(request, 'Your account has been successfully registered! Please login.', extra_tags='success')
    return redirect('login')

  return render(request, 'users/register.html' , {'specialities':specialities})


def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Try to authenticate AdminUser
        try:
            admin_user = AdminUser.objects.get(username=username)
            if admin_user.check_password(password):
                # Check if user is active
                if not admin_user.is_active or not admin_user.is_active_admin:
                    messages.error(request, 'Your admin account is inactive. Please contact system administrator.')
                    return render(request, 'users/admin_login.html')
                
                # Check if corresponding Admins entry exists
                try:
                    admin = Admins.objects.get(user=admin_user)
                    if not admin.is_active:
                        messages.error(request, 'Your admin privileges are inactive. Please contact system administrator.')
                        return render(request, 'users/admin_login.html')
                except Admins.DoesNotExist:
                    messages.error(request, 'Admin privileges not found. Please contact system administrator.')
                    return render(request, 'users/admin_login.html')

                # Store admin info in session instead of using Django's login
                request.session['admin_user_id'] = admin_user.id
                request.session['is_admin_logged_in'] = True
                
                messages.success(request, f'Welcome back, {admin_user.get_full_name() or admin_user.username}!')
                return redirect('admin_dashboard')
            else:
                messages.error(request, 'Incorrect username or password')
        except AdminUser.DoesNotExist:
            messages.error(request, 'Admin account not found')
            
        return render(request, 'users/admin_login.html')
    
    return render(request, 'users/admin_login.html')


def admin_logout(request):
    # Clear admin session data
    request.session.flush()
    messages.success(request, 'You have been successfully logged out.')
    return redirect('admin_login')


def login_view(request):
  if request.method == 'POST':
    username = request.POST.get('username')
    password = request.POST.get('password')

    user = authenticate(request, username=username, password=password)

    if user is not None:
      login(request, user)

      if user.is_doctor:
        return redirect('doctor_dashboard')

      elif Patients.objects.filter(user=user).exists():
        return redirect('patient_dashboard')
      
      else:
        # Regular user without specific role
        return redirect('user_dashboard')  # You may want to create this
    else:
      messages.error(request, 'Incorrect username or password')
      
    return render(request, 'users/login.html')
  
  return render(request, 'users/login.html')


def forgot_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = Users.objects.filter(email=email)
        if user:
            token = str(uuid.uuid4())
            reset = Reste_token.objects.create(
                user=user[0],
                email=user[0].email,  
                token=token  
            )
            reset.save()
            sent = send_email(user[0].email,token)
            if sent:
                return render(request, 'users/forgot.html',context={'send_email_succes': 1})
        else:
            return render(request, 'users/forgot.html', context={'errorlogin': 1})
    return render(request, 'users/forgot.html')

def reset_view(request,token):
    if request.method == 'POST':
        reste = Reste_token.objects.filter(token=token)
        print(reste)
        if reste:
            password = request.POST.get('password')
            confirm_password = request.POST.get('conf_password')
            if len(password) < 6:
                messages.error(request, 'Password must be at least 6 characters long.')
                return render(request, 'users/reset.html', {'token': token} )
            print(password)
            print(confirm_password)
            if password != confirm_password:
                messages.error(request, 'password do not match')
                return render(request, 'users/reset.html', {'token': token} )
            user = Users.objects.filter(email=reste[0].email).first()
            if user:
                hashed_password = make_password(password)
                user.password = hashed_password
                user.save()
                reste.delete()
                return redirect('login')
            else:
                return render(request, 'users/reset.html', {'token': token , 'errorlogin':1} )
        return render(request, 'users/reset.html', {'token': token} )
    return render(request, 'users/reset.html',{'token': token})


@login_required(login_url='/login')
def logout_view(request):
    logout(request)
    return redirect('login')
