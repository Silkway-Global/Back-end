from django.contrib import admin
from .models import Appointment
from accounts.choices import UserTypeChoices

class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('owner', 'preferred_date', 'preferred_time', 'created_at')
    list_filter = ('preferred_date', 'created_at')
    search_fields = ('owner__email', 'owner__full_name')
    
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

admin.site.register(Appointment, AppointmentAdmin)
