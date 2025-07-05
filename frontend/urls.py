from . import views 
from django.urls import path

app_name = 'frontend'

urlpatterns = [
    path('', views.index, name='index'),
    path('terms/', views.terms, name='terms'),
    path('waitlist/', views.waitlist, name='waitlist'),
]

