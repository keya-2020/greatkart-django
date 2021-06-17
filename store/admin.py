from django.contrib import admin
from .models import Products

# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('product_name',)}
    list_display        = ('product_name', 'price','category', 'slug','modified_date')

admin.site.register(Products, ProductAdmin)

