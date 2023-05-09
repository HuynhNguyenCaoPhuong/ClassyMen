from django.contrib import admin
from .models import Customer
from wishlist.models import Wishlist


class WishlistItemInline(admin.StackedInline):
    model = Wishlist
    extra = 0
    readonly_fields = ['product', 'user', 'name', 'quantity', 'price', 'image_product']


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    readonly_fields = ('user', 'username', 'tel', 'address', 'first_name', 'last_name', 'email')
    list_filter = ('user__username', 'tel') 
    search_fields = ('user__username', 'tel', 'user__first_name', 'user__last_name', 'user__email')

    inlines = [WishlistItemInline]

    def username(self, obj):
        return obj.user.username
    
    def first_name(self, obj):
        return obj.user.first_name
    
    def last_name(self, obj):
        return obj.user.last_name
    
    def email(self, obj):
        return obj.user.email

