from rest_framework import permissions
from core.models import UserOrganization
from core.choices import StatusChoices, RoleChoices


class IsSuperuser(permissions.IsAdminUser):
    def has_permission(self, request, view):
        return request.user.is_superuser
    
class IsOrganizationInternal(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        return UserOrganization.objects.filter(user=request.user, role__in = ['owner', 'admin', 'manager', 'staff'], status=StatusChoices.Active).exists()
    
class IsOrganizationOwner(permissions.BasePermission):
    
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        return UserOrganization.objects.filter(user=request.user, role = RoleChoices.Owner, status = StatusChoices.Active).exists()
        
class IsOrganizationAdmin(IsOrganizationOwner):
    
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        if super().has_permission(request, view):
            return True
        
        return UserOrganization.objects.filter(user=request.user, role = RoleChoices.Admin, status = StatusChoices.Active).exists()
    
class IsOrganizationManager(IsOrganizationAdmin):
    
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        if super().has_permission(request, view):
            return True
        
        return UserOrganization.objects.filter(user=request.user, role = RoleChoices.Manager, status = StatusChoices.Active).exists()
    
class IsOrganizationStaff(IsOrganizationManager):
    
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        if super().has_permission(request, view):
            return True
        
        return UserOrganization.objects.filter(user=request.user, role = RoleChoices.Staff, status = StatusChoices.Active).exists()
    

    

    

    