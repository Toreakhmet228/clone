from django.contrib import admin
from .models import Category, SubCategory, Product, ProductImage, ProductReview, Cart, CartItem, Order

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'category', 'subcategory', 'stock', 'created_at')
    search_fields = ('title', 'category__name', 'subcategory__name')
    list_filter = ('category', 'subcategory')
    inlines = [ProductImageInline]

class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'created_at')
    search_fields = ('product__title', 'user')
    list_filter = ('rating',)

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 1

class CartAdmin(admin.ModelAdmin):
    list_display = ('user',)
    search_fields = ('user',)
    inlines = [CartItemInline]

class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'order_date', 'status')
    search_fields = ('user',)
    list_filter = ('status',)

admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductReview, ProductReviewAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(Order, OrderAdmin)
