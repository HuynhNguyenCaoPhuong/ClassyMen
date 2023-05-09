from django.urls import path
from . import views

app_name = 'store'
urlpatterns = [
    path('', views.index, name='index'),
    path('shop/<slug:slug>/', views.shop, name='shop'),
    path('detail/<int:id>/', views.detail, name='detail'),
    path('search/', views.search, name='search'),
    path('contact/', views.contact, name='contact'),
    path('faqs/', views.faqs, name='faqs'),
]