from django.contrib import admin
from .models import Category, Product, Order, OrderItem, Banner

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'image')

@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'active')
    list_editable = ('order', 'active')

admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)