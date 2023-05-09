from django.contrib import admin
from . import models

@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    ordering = ['name']
    list_display = ['name', 'slug']
    search_fields = ['name']


@admin.register(models.SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    autocomplete_fields = ['category']
    prepopulated_fields = {
        'slug': ['name']
    }
    list_display = ['name', 'img', 'slug', 'category_name']
    search_fields = ['name']

    def category_name(self, subcategory):
        return subcategory.category.name
    

@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    autocomplete_fields = ['subcategory']
    list_display = ['name', 'price', 'price_origin', 'subcategory']
    list_filter = ['public_day', 'subcategory']
    list_editable = ['price', 'price_origin']
    search_fields = ['name__istartswith']
    list_per_page = 10

    def category_name(self, product):
        return product.subcategory.name

    @admin.display(ordering='viewed')
    def viewed_status(self, product):
        if product.viewed == 0:
            return 'No'
        return 'Yes'