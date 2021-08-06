from django.contrib import admin
from .models import Products, Variation, ReviewRating

# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('product_name',)}
    list_display        = ('product_name', 'price','category', 'slug','modified_date')

class VariatonAdmin(admin.ModelAdmin):    
    list_display        = ('product', 'variation_category','variation_value', 'is_active','created_date')
    list_editable       =('is_active',)# rendre un champs editable
    list_filter         = ('product', 'variation_category','variation_value')
admin.site.register(Products, ProductAdmin)
admin.site.register(Variation,VariatonAdmin)
admin.site.register(ReviewRating)

