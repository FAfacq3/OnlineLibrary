from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('materials/', views.material_list, name='material_list'),
    path('materials/<int:material_id>/', views.material_detail, name='material_detail'),
    path('materials/upload/', views.upload_material, name='upload_material'),
    path('materials/<int:material_id>/download/', views.download_material, name='download_material'),
    path('materials/<int:material_id>/review/', views.add_review, name='add_review'),
    path('dashboard/', views.user_dashboard, name='user_dashboard'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
]
