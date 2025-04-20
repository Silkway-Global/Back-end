from django.contrib import admin
from .models import ContactMessage
from accounts.choices import UserTypeChoices

class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('subject', 'owner', 'sent_at')
    list_filter = ('sent_at',)
    search_fields = ('subject', 'message', 'owner__email', 'owner__full_name')
    
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

admin.site.register(ContactMessage, ContactMessageAdmin)