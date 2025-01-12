from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.product_list, name='product_list'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    path('category/<slug:category>/', views.category_products, name='category_products'),
    path('cart/', views.cart, name='cart'),
    path('cart/add/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/', views.update_cart, name='update_cart'),
    path('cart/remove/', views.remove_from_cart, name='remove_from_cart'),
    path('profile/', views.profile, name='profile'),
    path('orders/', views.orders, name='orders'),
    path('favorites/', views.favorites, name='favorites'),
    path('favorites/toggle/', views.toggle_favorite, name='toggle_favorite'),
    path('seller-center/', views.seller_center, name='seller_center'),
    path('seller/add-product/', views.add_product, name='add_product'),
    path('seller/edit-product/<int:pk>/', views.edit_product, name='edit_product'),
    path('seller/delete-product/<int:pk>/', views.delete_product, name='delete_product'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('policies/', views.policies, name='policies'),
    path('search/', views.search, name='search'),
]
