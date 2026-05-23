from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    # 'ordering' থেকে 'username' সরিয়ে দিন
    ordering = ('phone_number',) 
    
    # অন্যান্য লিস্ট ডিসপ্লে ঠিক রাখুন
    list_display = ('phone_number', 'full_name', 'email', 'is_staff')
    search_fields = ('phone_number', 'full_name')
    
    # fieldsets ঠিক রাখুন
    fieldsets = (
        (None, {'fields': ('phone_number', 'password')}),
        ('Personal Info', {'fields': ('full_name', 'email', 'address')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    
    # 'add_fieldsets' যোগ করুন যাতে ইউজার ক্রিয়েট করার সময় ঝামেলা না হয়
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone_number', 'password'),
        }),
    )