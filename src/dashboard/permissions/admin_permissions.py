
from rest_framework.permissions import BasePermission

class IsSuperAdminUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_super_admin