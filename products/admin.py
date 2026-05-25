from django.contrib import admin
from django.utils.html import format_html
from .models import Blog, Category, Brand, DynamicSection, Product, ProductVariant, Banner, Review
from .models import Coupon 
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
    list_display = ('id', 'name', 'category', 'brand', 'price', 'discount_price', 'stock', 'is_featured')
    list_filter = ('category', 'brand', 'is_featured')
    search_fields = ('name', 'description')
    list_editable = ('price', 'discount_price', 'stock', 'is_featured')
    inlines = [ProductVariantInline]

@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'name', 'sku', 'price_adjustment', 'stock')
    search_fields = ('product__name', 'sku', 'name')
    list_filter = ('product',)

@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    # image_preview যোগ করা হয়েছে যাতে লিস্টে ছবি দেখা যায়
    list_display = ('id', 'image_preview', 'title', 'position', 'is_active')
    list_filter = ('position', 'is_active')
    search_fields = ('title',)
    # লিস্ট থেকেই দ্রুত পজিশন বা স্ট্যাটাস চেঞ্জ করার জন্য
    list_editable = ('position', 'is_active') 

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="120" style="border-radius: 5px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);" />', obj.image.url)
        return "No Image"
    
    image_preview.short_description = 'Banner Preview'

@admin.register(DynamicSection)
class DynamicSectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    filter_horizontal = ('products',) # একাধিক প্রোডাক্ট সুন্দরভাবে সিলেক্ট করার জন্য

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'rating', 'is_verified', 'is_active')
    list_editable = ('is_active', 'is_verified')

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'created_at', 'is_active')
    list_editable = ('is_active',)
    

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount_amount', 'minimum_order_amount', 'valid_from', 'valid_to', 'is_active')
    list_filter = ('is_active', 'valid_from', 'valid_to')
    search_fields = ('code',)
    list_editable = ('is_active',) # লিস্ট থেকেই অন/অফ করার জন্য