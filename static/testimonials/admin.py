from django.contrib import admin
from .models import Testimonial
from accounts.choices import UserTypeChoices

class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('owner', 'university', 'country', 'created_at')
    list_filter = ('country', 'created_at')
    search_fields = ('owner__email', 'owner__full_name', 'university', 'story')
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.user_type == UserTypeChoices.ADMIN:
            return qs
        return qs.filter(owner=request.user)
    
    def has_change_permission(self, request, obj=None):
        if request.user.user_type == UserTypeChoices.ADMIN:
            return True
        if obj is not None:
            return obj.owner == request.user
        return True
    
    def has_delete_permission(self, request, obj=None):
        if request.user.user_type == UserTypeChoices.ADMIN:
            return True
        if obj is not None:
            return obj.owner == request.user
        return True
        
    def has_view_permission(self, request, obj=None):
        if request.user.user_type == UserTypeChoices.ADMIN:
            return True
        if obj is not None:
            return obj.owner == request.user
        return True
    
    def save_model(self, request, obj, form, change):
        if not change:  # If this is a new object
            obj.owner = request.user
        super().save_model(request, obj, form, change)

admin.site.register(Testimonial, TestimonialAdmin)