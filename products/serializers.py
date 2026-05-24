from rest_framework import serializers
from .models import Blog, DynamicSection, Product, ProductVariant, Category, Brand, Banner, Review

from rest_framework import serializers
from .models import Category, Product

class CategorySerializer(serializers.ModelSerializer):
    # Proti category-r top 5 products dynamic bhabe anar jonno
    top_products = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'icon', 'top_products']

    def get_top_products(self, obj):
        # Oi category-r prothom 5-ti product kora hocche
        products = Product.objects.filter(category=obj)[:5]
        # Request context pass kora hocche jate image-er full link pay
        return ProductSerializer(products, many=True, context=self.context).data

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'

class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = '__all__'

class VariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    variants = VariantSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = '__all__'
        brand_details = BrandSerializer(source='brand', read_only=True)
        
class DynamicSectionSerializer(serializers.ModelSerializer):
    # ডায়নামিক সেকশনের ভেতরে প্রোডাক্টের পুরো ডেটা পাঠানোর জন্য
    products = ProductSerializer(many=True, read_only=True) 

    class Meta:
        model = DynamicSection
        fields = ['id', 'title', 'products', 'order']

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = '__all__'