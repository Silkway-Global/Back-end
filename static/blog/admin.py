from django.contrib import admin
from .models import BlogPost
from accounts.choices import UserTypeChoices

class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'category', 'created_at', 'updated_at')
    list_filter = ('category', 'created_at')
    search_fields = ('title', 'content', 'owner__email', 'owner__full_name')
    prepopulated_fields = {'slug': ('title',)}
    
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

admin.site.register(BlogPost, BlogPostAdmin)
