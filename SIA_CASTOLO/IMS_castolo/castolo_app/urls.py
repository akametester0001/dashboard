from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='dashboard'),
    path('dashboard/', views.index, name='index'),
    path('animals/<int:pk>/edit/', views.animal_update, name='animal_update'),
    path('animals/<int:pk>/delete/', views.animal_delete, name='animal_delete'),
]
