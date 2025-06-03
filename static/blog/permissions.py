from rest_framework.permissions import BasePermission, SAFE_METHODS
from accounts.choices import UserTypeChoices

class AdminPostDeleteOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in ['POST', 'DELETE']:
            return (
                request.user.is_authenticated and 
                request.user.user_type == UserTypeChoices.ADMIN
            )
        return True  # разрешить другие методы (GET, PUT и т.п.)
