from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

class Address(models.Model):
    id_address = models.AutoField(primary_key=True)
    address_line = models.CharField(max_length=50)
    region = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    code_postal = models.CharField(max_length=50)
    
    class Meta:
      verbose_name = "Address"
      verbose_name_plural = "Addresses"
      
    def __str__(self):
      return self.address_line

class AdminUser(AbstractUser):
    # Admin-specific fields
    hospital_name = models.CharField(max_length=100)
    employee_id = models.CharField(max_length=20, unique=True)
    department = models.CharField(max_length=50, choices=[
        ('IT', 'Information Technology'),
        ('HR', 'Human Resources'),
        ('Finance', 'Finance'),
        ('Operations', 'Operations'),
        ('Management', 'Management'),
        ('Medical', 'Medical Administration'),
    ])
    hire_date = models.DateField()
    phone = models.CharField(max_length=15, blank=True, null=True)
    profile_avatar = models.ImageField(upload_to="admin/profiles", blank=True, default="admin/profiles/default.png", null=True)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True, related_name='admin_users')
    is_active_admin = models.BooleanField(default=True)
    
    # Fix reverse accessor conflicts
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='admin_users',
        related_query_name='admin_user',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='admin_users',
        related_query_name='admin_user',
    )
    
    class Meta:
        verbose_name = "AdminUser"
        verbose_name_plural = "AdminUsers"

    def __str__(self):
        return f"{self.get_full_name()} ({self.employee_id})" if self.get_full_name() else self.username

class Users(AbstractUser):
    email = models.CharField(max_length=50,unique=True)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=200)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50, null=True, blank=True, default="Hospital")
    gender_choices = (("Male", "Male"), ("Female", "Female"))
    gender = models.CharField(max_length=10, choices=gender_choices, default="not_known")
    birthday = models.DateField(null=True, blank=True)
    is_doctor = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    profile_avatar = models.ImageField(upload_to="users/profiles", blank=True, default="doctor/profiles/download.png", null=True)
    id_address = models.ForeignKey(Address, on_delete=models.CASCADE, null=True, related_name='regular_users')
    
    # Fix reverse accessor conflicts
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='regular_users',
        related_query_name='regular_user',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='regular_users',
        related_query_name='regular_user',
    )
    
    class Meta:
      verbose_name = "User"
      verbose_name_plural = "Users"
      
    def __str__(self):
      return self.username

class Reste_token(models.Model):
   user = models.ForeignKey(Users,on_delete=models.CASCADE)
   email = models.CharField(max_length = 50,unique=True)
   token = models.CharField(max_length = 50)

class Specialty(models.Model):
    name = models.CharField(max_length=25 , unique=True)
    description = models.TextField()
    
    class Meta:
      verbose_name = "Specialty"
      verbose_name_plural = "Specialty"
    
    def __str__(self):
      return self.name
    
class Doctors(models.Model):
  user = models.OneToOneField(Users, on_delete=models.CASCADE, primary_key=True)
  specialty = models.ForeignKey(Specialty,on_delete=models.CASCADE)
  bio = models.TextField()
  
  class Meta:
    verbose_name = "Doctor"
    verbose_name_plural = "Doctors"
    
  def __str__(self):
      return self.user.get_full_name() or self.user.username

class Admins(models.Model):
    user = models.OneToOneField(AdminUser, on_delete=models.CASCADE, primary_key=True)
    role = models.CharField(max_length=50, choices=[
        ('super_admin', 'Super Administrator'),
        ('system_admin', 'System Administrator'),
        ('hospital_admin', 'Hospital Administrator'),
        ('department_admin', 'Department Administrator'),
        ('staff_admin', 'Staff Administrator'),
    ])
    access_level = models.CharField(max_length=20, choices=[
        ('read', 'Read Only'),
        ('write', 'Read & Write'),
        ('admin', 'Full Admin'),
        ('super', 'Super Admin'),
    ], default='read')
    permissions = models.ManyToManyField(Permission, blank=True, related_name='admin_permissions')
    created_by = models.ForeignKey(AdminUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_admins')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    notes = models.TextField(blank=True, help_text="Administrative notes about this admin user")
    
    class Meta:
        verbose_name = "Admin"
        verbose_name_plural = "Admins"
    
    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} - {self.get_role_display()}"
      
class Patients(models.Model):
  user = models.OneToOneField(Users, on_delete=models.CASCADE, primary_key=True)
  insurance = models.CharField(max_length=50)
  
  class Meta:
    verbose_name = "Patient"
    verbose_name_plural = "Patients"
  
  def __str__(self):
      return self.user.get_full_name() or self.user.username

