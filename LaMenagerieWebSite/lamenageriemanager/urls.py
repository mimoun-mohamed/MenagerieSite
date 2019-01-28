from django.urls import path

from . import views

app_name = 'lamenageriemanager'
urlpatterns = [
    path('', views.index, name='index'),
    path('animals/list/', views.animals_list, name='animals_list'),
    path('animals/add/', views.animal_add, name='animal_add'),
    path('animals/<int:pk>/', views.animal_detail, name='animal_detail'),
    path('animals/<int:pk>/feed/', views.feed, name='feed'),
    path('animals/<int:pk>/entertain/', views.entertain, name='entertain'),
    path('animals/<int:pk>/sleep/', views.sleep, name='sleep'),
    path('animals/<int:pk>/wake_up/', views.wake_up, name='wake_up'),
    path('equipments/list/', views.equipments_list, name='equipments_list'),
    path('equipments/add/', views.equipment_add, name='equipment_add'),
    path('equipments/<int:pk>/', views.equipment_detail, name='equipment_detail'),
    path('equipments/<int:pk>/free/', views.equipment_free, name='equipment_free')

]