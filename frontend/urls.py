from frontend.views import main, waitlist, product, legal, order, contact
from django.urls import path

app_name = 'frontend'

urlpatterns = [
    # Main
    path('', main.index, name='index'),
    # Contact 
    path("contact", contact.create, name="create_message"),
    # Legal
    path('terms/', legal.terms, name='terms'),

    # WaitList
    path('waitlist/', waitlist.waitlist, name='waitlist'),

    # Product
    path('<str:shop_code>/<int:pk>', product.product_landing, name='product_landing'),

    # Order
    path('get-communes/<int:province_id>/<str:lang_code>/', order.getCommunes, name='getCommunes'),
    path("submit-order/<int:product_id>/", order.submit_order, name="submit_order"),

]

