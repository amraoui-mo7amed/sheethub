from django.urls import path
from .views import dash, users, waitlist, smtp, notifications, products

app_name = 'dash'  # Changed from 'dashboard' to match the namespace in the template

urlpatterns = [
    path('', dash.home, name='home'),
    # Users 
    path('users/', users.list.as_view(), name='users_list'),
    path('users/profile/<int:pk>', users.userProfile, name='user_profile'),
    path('users/profile/edit', users.profileEdit, name='user_profile_edit'),
    path('users/delete/<int:pk>', users.Delete, name='user_delete'),
    # Notifications 
    path("notifications/", notifications.get_notifications , name="notifications"),
    path("notifications/mark-all-read/", notifications.set_read , name="mark_all_read"),
    # Products 
    path('products/', products.list, name='products_list'),
    path('products/create/', products.create, name='product_create'),
    path('products/delete/<int:pk>', products.Delete, name='product_delete'),
    path('products/details/<int:pk>', products.productDetails, name='product_details'),
    # Waitlist
    path('waitlist/', waitlist.List.as_view(), name='waitlist'),
    # SMTP Server
    path('smtp/', smtp.SMTPConfigDetails, name='smtp_config'),
    path('smtp/update/', smtp.update_smtp_config, name='update_smtp_config'),
    path('smtp/test-connection/', smtp.test_connection, name='test_smtp_connection'),
    path('smtp/delete/<int:pk>', smtp.Delete, name='smtp_delete'),
]