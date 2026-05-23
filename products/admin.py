from django.contrib import admin
from .models import Blog, Category, Brand, DynamicSection, Product, ProductVariant, Banner, Review

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'brand', 'price', 'stock', 'is_featured')
    list_filter = ('category', 'brand', 'is_featured')
    search_fields = ('name', 'description')
    list_editable = ('price', 'stock', 'is_featured')
    inlines = [ProductVariantInline]

@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'name', 'sku', 'price_adjustment', 'stock')
    search_fields = ('product__name', 'sku', 'name')
    list_filter = ('product',)

@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'position', 'is_active')
    list_filter = ('position', 'is_active')
    search_fields = ('title',)
    
@admin.register(DynamicSection)
class DynamicSectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    filter_horizontal = ('products',) # একাধিক প্রোডাক্ট সুন্দরভাবে সিলেক্ট করার জন্য

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'rating', 'is_verified', 'is_active')

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'created_at', 'is_active')