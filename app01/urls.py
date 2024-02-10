
from django.contrib import admin
from django.urls import path, re_path
from app01 import views

urlpatterns = [
    path('index/', views.index),
    path('login/', views.login),
    path('getvalidCode/', views.getvalidCode),
    path('register/', views.register),
    path('logout/', views.logout),
    path('upup/', views.upup),
    path('comment/', views.comment),
    path('set_tree/', views.set_tree),
    path('cn_backend/', views.cn_backend),
    path('add_article/', views.add_article),
    path('edit_article/', views.edit_article),
    path('delete_article/', views.delete_article),
    path('add_tag/', views.add_tag),
    path('add_category/', views.add_category),
    path('<str:username>/arciles/<int:arcile_id>/', views.arcile_datatil),
    path('<str:username>/', views.home_site),
    path('<str:username>/<str:tag>/<str:param>/', views.home_site),


]
