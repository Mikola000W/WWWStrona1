from django.contrib import admin
from django.urls import path

from customers import views as customer_views
from items import views as item_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('customers/new/', customer_views.customer_create, name="customer_create"),
    path('customers/t/', customer_views.customer_table, name="customer_table"),
    path('customers/<int:pk>/', customer_views.customer_detail,
         name="customer_detail"),
    path('customers/<int:pk>/edit', customer_views.customer_update,
         name="customer_update"),
    path('customers/', customer_views.customer_list, name="customer_list"),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('', customer_views.home, name="home"),

    path('items/new/', item_views.item_create, name="item_create"),
    path('items/t/', item_views.item_table, name="item_table"),
    path('items/', item_views.item_list, name="item_list"),
    path('cart/', item_views.cart, name="cart"),
    path('add-to-cart/<int:item_id>', item_views.add_to_cart, name="add_to_cart"),
    path('delete-from-cart/', item_views.delete_from_cart, name="delete_from_cart"),

]

