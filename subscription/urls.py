from django.urls import path
from . import views

app_name = 'subs'

urlpatterns = [
    path('plans/', views.PlanListView.as_view(), name='plans'),
    path('plans/create/', views.create, name='create_plan'),
    path("plans/delete/<int:pk>", views.Delete, name = "delete_subscription")
]
