from django.urls import path
from . import views

app_name = 'wishlist'
urlpatterns = [
    path('', views.wishlist, name='wishlist'),
    path('add/', views.add, name='add'),
    path('remove/', views.remove, name='remove'),
]