from django.db import models
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    icon = models.ImageField(upload_to='categories/icons/', blank=True, null=True)

    def __str__(self):
        return self.name

class Brand(models.Model):
    name = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='brands/logos/', blank=True, null=True)
    
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    stock = models.IntegerField()
    is_featured = models.BooleanField(default=False)
    # ফ্রন্টএন্ডে ছবি দেখানোর জন্য thumbnail ফিল্ড অ্যাড করা হলো
    thumbnail = models.ImageField(upload_to='products/thumbnails/', blank=True, null=True)
    

    def __str__(self):
        return self.name

class ProductVariant(models.Model):
    product = models.ForeignKey(Product, related_name='variants', on_delete=models.CASCADE)
    name = models.CharField(max_length=50) # e.g., '8GB/128GB' or 'Red'
    price_adjustment = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    stock = models.IntegerField(default=0)
    sku = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"{self.product.name} - {self.name}"
    
class Banner(models.Model):
    POSITION_CHOICES = (
        ('hero_carousel', 'Hero Carousel'),
        ('hero_side_top', 'Hero Side Top'),
        ('hero_side_bottom', 'Hero Side Bottom'),
        
        # নতুন যোগ করা হলো আপনার স্পেসিফিক লেআউটের জন্য
        ('category_banner', 'After Category (50-50)'), 
        ('brand_banner', 'After Brands (100% Width)'), 
        ('pre_review_banner', 'Before Reviews (60-40)'),
    )
    title = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(upload_to='banners/')
    position = models.CharField(max_length=50, choices=POSITION_CHOICES)
    link = models.URLField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.position} - {self.title}"
    
# ডায়নামিক সেকশন (যেমন: New Arrivals, Trending)
class DynamicSection(models.Model):
    title = models.CharField(max_length=255)
    products = models.ManyToManyField(Product, related_name='dynamic_sections')
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0, help_text="সেকশনটি কত নম্বরে দেখাবে")

    def __str__(self):
        return self.title

# কাস্টমার রিভিউ
class Review(models.Model):
    customer_name = models.CharField(max_length=100)
    rating = models.IntegerField(default=5)
    comment = models.TextField()
    is_verified = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.customer_name

# ব্লগ সেকশন
class Blog(models.Model):
    title = models.CharField(max_length=255)
    category = models.CharField(max_length=100, default="GADGETS")
    excerpt = models.TextField(help_text="ব্লগের শর্ট ডেসক্রিপশন")
    image = models.ImageField(upload_to='blogs/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title
    


class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True, help_text="কুপন কোড (যেমন: EID50, NEWYEAR200)")
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, help_text="কত টাকা ডিসকাউন্ট হবে")
    minimum_order_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, help_text="মিনিমাম কত টাকার অর্ডার করতে হবে")
    valid_from = models.DateTimeField(help_text="কবে থেকে কুপনটি কাজ করবে")
    valid_to = models.DateTimeField(help_text="কবে কুপনটির মেয়াদ শেষ হবে")
    is_active = models.BooleanField(default=True, help_text="কুপনটি অ্যাক্টিভ আছে কি না")

    def __str__(self):
        return self.code

    # কুপনটি বর্তমানে ভ্যালিড কি না তা চেক করার কাস্টম মেথড
    def is_valid(self):
        now = timezone.now()
        return self.is_active and self.valid_from <= now <= self.valid_to