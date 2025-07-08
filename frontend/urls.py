from . import views 
from django.urls import path

app_name = 'frontend'

urlpatterns = [
    path('', views.index, name='index'),
    path('terms/', views.terms, name='terms'),
    path('waitlist/', views.waitlist, name='waitlist'),
    path('<str:shop_code>/<int:pk>', views.product_landing, name='product_landing'),
    path('get-communes/<int:province_id>/', views.getCommunes, name='getCommunes'),
]

