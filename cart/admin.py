from django.contrib import admin
from . import models


class OrderItemInline(admin.TabularInline):
    model = models.OrderItem
    extra = 0
    readonly_fields = ['product', 'quantity', 'size', 'color', 'vote', 'price']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if 'object_id' in request.resolver_match.kwargs:
            order_id = request.resolver_match.kwargs['object_id']
            qs = qs.filter(order_id=order_id)
        else:
            qs = qs.none()
        return qs

    def get_formset(self, request, obj=None, **kwargs):
        self.parent_obj = obj
        return super().get_formset(request, obj=obj, **kwargs)


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    ordering = ['username']
    list_display = ['username', 'status', 'total', 'address']
    search_fields = ['username__istartswith']
    list_filter = ['created', 'total']
    inlines = [OrderItemInline]


@admin.register(models.OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    autocomplete_fields = ['order']
    list_display = ['product', 'order', 'quantity', 'size', 'color', 'vote']
    search_fields = ['product__istartswith']
    list_per_page = 20

