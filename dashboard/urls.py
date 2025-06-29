from django.urls import path
from .views import dash, users, waitlist, smtp

app_name = 'dash'  # Changed from 'dashboard' to match the namespace in the template

urlpatterns = [
    path('', dash.home, name='home'),
    # Users 
    path('users/', users.list.as_view(), name='users_list'),
    path('users/profile/<int:pk>', users.userProfile, name='user_profile'),
    path('users/delete/<int:pk>', users.Delete, name='user_delete'),
    # Waitlist
    path('waitlist/', waitlist.List.as_view(), name='waitlist'),
    # SMTP Server
    path('smtp/', smtp.SMTPConfigDetails, name='smtp_config'),
    path('smtp/update/', smtp.update_smtp_config, name='update_smtp_config'),
    path('smtp/test-connection/', smtp.test_connection, name='test_smtp_connection'),
    path('smtp/delete/<int:pk>', smtp.Delete, name='smtp_delete'),
]