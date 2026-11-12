from django.urls import path
from .import views

urlpatterns=[
    path('',views.home,name='home'),
    path('register/',views.register,name='register'),
    path('add-staff/', views.add_staff, name='add_staff'),
    path('resident-login/',views.resident_login,name='resident_login'),
    path('admin-login/',views.admin_login,name='admin_login'),
    path('staff-login/',views.staff_login,name='staff_login'),
    path('resdient-dashboard/',views.resident_dashboard,name='resident_dashboard'),
    path('admin-dashboard/',views.admin_dashboard,name='admin_dashboard'),
    path('staff-dashboard/',views.staff_dashboard,name='staff_dashboard'),
    path('logout/',views.user_logout,name='logout'),
]