from django.urls import path
from . import views
from django.contrib import admin
from django.urls import include, path
from django.conf import settings 
from django.conf.urls.static import static
urlpatterns = [
    path('', views.home, name='home'),
    path('optimize/', views.optimize_route, name='optimize_route'),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
