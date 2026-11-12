from django.urls import path
from .import views

urlpatterns=[
    path('create/', views.complaint_create, name='complaint_create'),

    path('detail/<int:pk>/', views.complaint_detail, name='complaint_detail'),

    path('assign/<int:pk>/', views.assign_complaint, name='assign_complaint'),

    path('take/<int:pk>/', views.take_complaint, name='take_complaint'),

    path('update/<int:pk>/', views.staff_update_complaint, name='staff_update_complaint'),
]