from django.urls import path
from .views import auth, forgot_password, email

app_name = 'user_auth'

urlpatterns = [
    path('login/', auth.signin, name='login'),
    path('logout/', auth.signout, name='logout'),
    path('register/', auth.signup, name='signup'),
    # path('profile/', views.profile_view, name='profile'),
    path('password-reset/', forgot_password.forgot_password, name='password_reset'),
    # path('password-reset/done/', views.password_reset_done, name='password_reset_done'),
    # path('reset/<uidb64>/<token>/', views.password_reset_confirm, name='password_reset_confirm'),
    # path('reset/done/', views.password_reset_complete, name='password_reset_complete'),
]