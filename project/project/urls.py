"""myproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.main_page, name='main'),
    path('about-us/', views.about_us, name='about'),
    path('contact-us/', views.contact_us, name='contact'),
    path('privacy-policy/', views.privacy_policy, name='privacypolicy'),
    path('terms-conditions/', views.terms_conditions, name='terms'),
    path('blog/', views.blogs, name='blog'),
    path('blog-single/', views.blog_single, name='blogSingle'),

    path('search/', views.search, name='search'),
    path('products/', views.product, name='product'),
    path('product/<str:uid>', views.single_product, name='singleProduct'),
    # path('cart', views.shopping_cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('register/', views.register, name='register'),
    path('login/', views.Handellogin, name='login'),
    path('logout/', views.HandelLogout, name='logout'),

    # Cart
    path('cart/add/<str:id>/<str:variant>/', views.cart_add, name='cart_add'),
    path('cart/item_clear/<str:id>/', views.item_clear, name='item_clear'),
    path('cart/item_increment/<str:id>/',views.item_increment, name='item_increment'),
    path('cart/item_decrement/<str:id>/', views.item_decrement, name='item_decrement'),
    path('cart/cart_clear/', views.cart_clear, name='cart_clear'),
    path('cart/cart-detail/',views.cart_detail,name='cart_detail'),

    path('create-order/', views.create_order, name='create_order'),
    path('place-order/', views.place_order, name='place_order'),
    path('check-order-status/', views.check_order, name='check_order_status'),

] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
