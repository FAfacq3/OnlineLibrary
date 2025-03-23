from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('materials/', views.material_list, name='material_list'),
    path('materials/<int:material_id>/', views.material_detail, name='material_detail'),
    path('materials/<int:material_id>/txt_preview/', views.txt_preview, name='txt_preview'),
    path('materials/random/', views.random_material, name='random_material'),
    path('materials/upload/', views.upload_material, name='upload_material'),
    path('materials/<int:material_id>/download/', views.download_material, name='download_material'),
    path('materials/<int:material_id>/favourite/', views.favourite_material, name='favourite_material'),
    path('materials/<int:material_id>/delete/', views.delete_material, name='delete_material'),
    path('materials/<int:material_id>/review/', views.add_review, name='add_review'),
    path('dashboard/', views.user_dashboard, name='dashboard'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),

]
