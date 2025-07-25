from django.urls import path
from .views import dash, users, waitlist, smtp, notifications, products, contacts, order, feedback

app_name = 'dash'  # Changed from 'dashboard' to match the namespace in the template

urlpatterns = [
    path('', dash.home, name='home'),
    # Users 
    path('users/', users.list.as_view(), name='users_list'),
    path('users/profile/<int:pk>', users.userProfile, name='user_profile'),
    path('users/profile/edit', users.profileEdit, name='user_profile_edit'),
    path('users/delete/<int:pk>', users.Delete, name='user_delete'),
    # Seller Data
    path("seller-data/", dash.seller_data, name="seller_data"),  
    # Notifications 
    path("notifications/", notifications.get_notifications , name="notifications"),
    path("notifications/mark-all-read/", notifications.set_read , name="mark_all_read"),
    # Products 
    path('products/', products.list, name='products_list'),
    path('products/create/', products.create_or_update_product, name='product_create'),
    path('products/edit/<int:pk>/', products.update_product, name='product_update'),
    path('products/delete/<int:pk>', products.Delete, name='product_delete'),
    path('products/details/<int:pk>', products.productDetails, name='product_details'),
    path('products/images/delete/<int:pk>', products.DeleteProductImage, name='product_image_delete'),
    # Waitlist
    path('waitlist/', waitlist.List.as_view(), name='waitlist'),
    # SMTP Server
    path('smtp/', smtp.SMTPConfigDetails, name='smtp_config'),
    path('smtp/update/', smtp.update_smtp_config, name='update_smtp_config'),
    path('smtp/test-connection/', smtp.test_connection, name='test_smtp_connection'),
    path('smtp/delete/<int:pk>', smtp.Delete, name='smtp_delete'),
    # Contacts 
    path('contacts/', contacts.List, name='contacts'),
    path('contacts/details/<int:pk>', contacts.details, name='contact_details'),
    path('contacts/reply/<int:contact_pk>', contacts.Reply, name='reply'),
    # Order 
    path('orders/update-status/', order.update_order_status, name='update_order_status'),
    # feedback 
    path('feedback/', feedback.feedback_list, name='feedback_list'),
    path('feedback/create/', feedback.create, name='create_feedback'),
]