
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve
from bokexit import settings
from app01 import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("blog/", include(('app01.urls', 'app01'))),
    path("", views.index),
    re_path(r"media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}),
    path('<str:username>/', views.home_site),
    path('<str:username>/<str:tag>/<str:param>/', views.home_site),
]
