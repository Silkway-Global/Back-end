from django.contrib import admin
from .models import CustomUser
from django.contrib.auth.admin import UserAdmin
from .choices import UserTypeChoices

class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'full_name', 'user_type', 'is_active', 'is_staff')
    list_filter = ('user_type', 'is_active', 'is_staff')
    search_fields = ('email', 'full_name', 'phone_number')
    ordering = ('email',)
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('full_name', 'phone_number')}),
        ('Permissions', {'fields': ('user_type', 'is_active', 'is_staff', 'is_superuser')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'full_name', 'password1', 'password2', 'user_type'),
        }),
    )
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.user_type == UserTypeChoices.ADMIN:
            return qs
        # Students can only see their own user account
        return qs.filter(id=request.user.id)
    
    def has_add_permission(self, request):
        return request.user.user_type == UserTypeChoices.ADMIN
    
    def has_change_permission(self, request, obj=None):
        if request.user.user_type == UserTypeChoices.ADMIN:
            return True
        # Students can only edit their own profile
        if obj is not None:
            return obj.id == request.user.id
        return True
    
    def has_delete_permission(self, request, obj=None):
        # Only admins can delete users
        return request.user.user_type == UserTypeChoices.ADMIN
    
    def has_view_permission(self, request, obj=None):
        if request.user.user_type == UserTypeChoices.ADMIN:
            return True
        # Students can only view their own profile
        if obj is not None:
            return obj.id == request.user.id
        return True
    
    def get_readonly_fields(self, request, obj=None):
        if request.user.user_type == UserTypeChoices.ADMIN:
            return ()
        # Students cannot change their user_type
        return ('user_type', 'is_staff', 'is_superuser')

admin.site.register(CustomUser, CustomUserAdmin)
