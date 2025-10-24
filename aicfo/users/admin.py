from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import AppUser, Company

# Register your models here.

class AppUserAdmin(UserAdmin):
    model=AppUser
    list_display = ['email', 'full_name', 'company', 'role', 'is_staff', 'is_superuser', 'date_joined', 'phone']
    list_filter = ('is_active', 'company', 'date_joined')
    search_fields = ('full_name', 'email')
    ordering = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}), 

        ('Personal Info', {'fields': ('full_name', 'phone')}),

        ('Company & Role', {'fields': ('company', 'role')}),

        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),

        ('Important dates', {'fields': ('date_joined',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'full_name', 'company', 'role', 'phone', 'password'), 
        }),
    )
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.select_related('company')
        return qs

class CompanyAdmin(admin.ModelAdmin):
    list_display = ['id','name','email','created_at', 'phone']
    list_filter = ('is_active', 'industry', 'created_at')
    search_fields = ('name', 'email', 'website')
    ordering = ('name',)
    fieldsets = (
        (None, {'fields': ('name', 'email', 'phone', 'website')}),

        ('Business Details', {'fields': ('industry',)}),

        ('Status & Tracking', {'fields': ('is_active', 'created_at', 'updated_at')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('name', 'email', 'phone', 'website', 'industry', 'is_active'), 
        }),
    )

    readonly_fields = ('created_at', 'updated_at')
    

admin.site.register(AppUser, AppUserAdmin)
admin.site.register(Company, CompanyAdmin)