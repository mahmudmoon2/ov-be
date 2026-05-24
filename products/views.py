from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Blog, DynamicSection, Product, Category, Brand, Banner, Review
from .serializers import (
    BlogSerializer,
    DynamicSectionSerializer,
    ProductSerializer, 
    CategorySerializer, 
    BrandSerializer, 
    BannerSerializer,
    ReviewSerializer,
    ReviewSerializer
)

# -------------------------
# Product Views
# -------------------------
class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

# -------------------------
# Homepage Dynamic Data View
# -------------------------
class HomepageDataView(APIView):
    def get(self, request):
        limited_sale = Product.objects.filter(stock__gt=0, stock__lt=10)[:10] 
        exclusive_products = Product.objects.filter(is_featured=True)[:10]
        active_sections = DynamicSection.objects.filter(is_active=True).order_by('order')
        reviews = Review.objects.filter(is_active=True).order_by('-id')[:3] 
        blogs = Blog.objects.filter(is_active=True).order_by('-created_at')[:3]

        # ইমেজের ফুল URL পাওয়ার জন্য context এ request পাস করা হচ্ছে
        context = {'request': request}

        return Response({
            'limited_sale': ProductSerializer(limited_sale, many=True, context=context).data,
            'exclusive_products': ProductSerializer(exclusive_products, many=True, context=context).data,
            'dynamic_sections': DynamicSectionSerializer(active_sections, many=True, context=context).data,
            'reviews': ReviewSerializer(reviews, many=True, context=context).data,
            'blogs': BlogSerializer(blogs, many=True, context=context).data,
        })

# -------------------------
# Other List Views
# -------------------------
class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class BrandListView(generics.ListAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer

class BannerListView(generics.ListAPIView):
    queryset = Banner.objects.filter(is_active=True)
    serializer_class = BannerSerializer
    

# products/views.py এর শেষে যোগ করুন
class BlogDetailView(generics.RetrieveAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer