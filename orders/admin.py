from django.contrib import admin
from .models import Payment, Order, OrderProduct


class orderProductInLine(admin.TabularInline):
    model = OrderProduct
    readonly_fields  = ('payment','user', 'product', 'quantity', 'product_price', 'ordered')
    extra = 0
    
class orderAdmin(admin.ModelAdmin):
    list_display = ['order_number','full_name','phone','email', 'city', 'order_total',
    'tax', 'status', 'is_ordered','created_at']
    list_filter = ['status','is_ordered']
    search_fields = ['status','first_name','last_name', 'phone', 'email']
    list_per_page = 20
    inlines = [orderProductInLine,]
# Register your models here.
admin.site.register(Payment)
admin.site.register(Order, orderAdmin)
admin.site.register(OrderProduct)