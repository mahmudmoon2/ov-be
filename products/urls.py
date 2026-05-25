from django.urls import path
from .views import (
    BlogDetailView,
    ProductListView, 
    ProductDetailView, 
    HomepageDataView, 
    CategoryListView,
    BrandListView,
    BannerListView,
    ApplyCouponView,
)

urlpatterns = [
    # Product Endpoints
    path('list/', ProductListView.as_view(), name='product-list'),
    path('details/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    
    # Homepage Data Endpoint
    path('homepage-data/', HomepageDataView.as_view(), name='homepage-data'),
    
    # Category, Brand, Banner Endpoints
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('brands/', BrandListView.as_view(), name='brand-list'),
    path('banners/', BannerListView.as_view(), name='banner-list'),
    path('blog/<int:pk>/', BlogDetailView.as_view(), name='blog-detail'),
    path('apply-coupon/', ApplyCouponView.as_view(), name='apply-coupon'),
]