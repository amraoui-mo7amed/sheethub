from django.urls import path
from .views import auth, password_reset, email

app_name = 'user_auth'

urlpatterns = [
    path('login/', auth.signin, name='login'),
    path('logout/', auth.signout, name='logout'),
    path('register/', auth.signup, name='signup'),
    # path('profile/', views.profile_view, name='profile'),
    path('password-reset/', password_reset.forgot_password, name='password_reset'),
    path('confirm-email/<str:token>/', email.confirm_email_view, name='confirm_email'),
    path('password-reset/confirm/<str:token>/', password_reset.password_reset_confirm, name='reset_password_confirm'),
]