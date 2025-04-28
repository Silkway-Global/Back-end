from django.contrib import admin

from accounts.choices import UserTypeChoices
from .models import Course

class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'country', 'price', 'duration_weeks', 'start_date')
    list_filter = ('category', 'country', 'start_date')
    search_fields = ('title', 'description', 'category', 'country')
    
    def has_add_permission(self, request):
        return request.user.user_type == UserTypeChoices.ADMIN
    
    def has_change_permission(self, request, obj=None):
        return request.user.user_type == UserTypeChoices.ADMIN
    
    def has_delete_permission(self, request, obj=None):
        return request.user.user_type == UserTypeChoices.ADMIN
    
    def has_view_permission(self, request, obj=None):
        # Everyone can view courses
        return True

admin.site.register(Course, CourseAdmin)