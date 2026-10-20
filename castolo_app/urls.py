from django.urls import path
from . import views


urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Owner URLs
    path('owners/', views.owner_list, name='owner_list'),
    path('owners/add/', views.owner_create, name='owner_create'),
    path('owners/<int:pk>/', views.owner_detail, name='owner_detail'),
    path('owners/<int:pk>/edit/', views.owner_update, name='owner_update'),
    path('owners/<int:pk>/delete/', views.owner_delete, name='owner_delete'),
    
    # Pet URLs
    path('pets/', views.pet_list, name='pet_list'),
    path('pets/add/', views.pet_create, name='pet_create'),
    path('pets/<int:pk>/', views.pet_detail, name='pet_detail'),
    path('pets/<int:pk>/edit/', views.pet_update, name='pet_update'),
    path('pets/<int:pk>/delete/', views.pet_delete, name='pet_delete'),
    
    # Visit URLs
    path('visits/', views.visit_list, name='visit_list'),
    path('visits/add/', views.visit_create, name='visit_create'),
    path('visits/<int:pk>/', views.visit_detail, name='visit_detail'),
    path('visits/<int:pk>/edit/', views.visit_update, name='visit_update'),
    path('visits/<int:pk>/delete/', views.visit_delete, name='visit_delete'),
]