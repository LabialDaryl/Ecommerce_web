from django.contrib import admin
from .models import Product, Order, OrderItem, Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'price', 'stock', 'category')
    list_filter = ('category',)
    search_fields = ('title', 'description')
    list_editable = ('price', 'stock')
    ordering = ('-id',)
    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'category')
        }),
        ('Pricing & Stock', {
            'fields': ('price', 'stock')
        }),
        ('Media', {
            'fields': ('image',)
        }),
    )


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'ordered_date', 'is_ordered', 'total_price')
    list_filter = ('is_ordered',)
    search_fields = ('user__username',)
    ordering = ('-ordered_date',)


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'product', 'quantity')
    search_fields = ('product__title', 'order__user__username')
    autocomplete_fields = ('product', 'order')
