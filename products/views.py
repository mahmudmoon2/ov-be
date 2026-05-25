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
from rest_framework import status
from .models import Coupon

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
    


class ApplyCouponView(APIView):
    def post(self, request):
        # রিঅ্যাক্ট থেকে আসা ডেটা রিসিভ করা হচ্ছে
        code = request.data.get('code')
        cart_total = request.data.get('cart_total', 0)

        try:
            # Case-insensitive চেক (user test50 বা TEST50 যাই দিক কাজ করবে)
            coupon = Coupon.objects.get(code__iexact=code)
            
            # কুপনের মেয়াদ বা অ্যাক্টিভ স্ট্যাটাস চেক
            if not coupon.is_valid():
                return Response({
                    'valid': False, 
                    'message': 'This coupon is expired or inactive.'
                })
            
            # মিনিমাম অর্ডার অ্যামাউন্ট চেক
            if float(cart_total) < float(coupon.minimum_order_amount):
                return Response({
                    'valid': False, 
                    'message': f'Minimum order amount should be ৳{coupon.minimum_order_amount}'
                })

            # সব ঠিক থাকলে সাকসেস রেসপন্স
            return Response({
                'valid': True,
                'discount_amount': coupon.discount_amount,
                'message': 'Coupon applied successfully!'
            })

        except Coupon.DoesNotExist:
            return Response({
                'valid': False, 
                'message': 'Invalid coupon code.'
            })