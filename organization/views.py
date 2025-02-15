from rest_framework import generics, serializers

from rest_framework.filters import SearchFilter


from core.choices import StatusChoices
from core.models import UserOrganization
from core import permissions as custom_permissions

from .serializers import (
    UserOrganizationSerializer, 
    OrganizationInternalSerializer,
    OrganizationInternalDetailsSerializer
    )
    
class ListOrganizationInternalMembersView(generics.ListAPIView):
    serializer_class = UserOrganizationSerializer
    permission_classes = [custom_permissions.IsOrganizationInternal]
    filter_backends = [SearchFilter]
    search_fields = ['username', 'role', 'status']
    
    
    def get_queryset(self):
        return UserOrganization.objects.filter(status__in = ['active', 'inactive']).select_related('user').order_by('pk')



class CreateOrganizationInternalView(generics.CreateAPIView):
    serializer_class = OrganizationInternalSerializer
    permission_classes = [custom_permissions.IsOrganizationInternal]
    filter_backends = [SearchFilter]
    search_fields = ['username', 'email', 'role', 'status']
    

class ListOrganizationInternalView(generics.ListAPIView):
    serializer_class = OrganizationInternalDetailsSerializer
    permission_classes = [custom_permissions.IsOrganizationInternal]
    filter_backends = [SearchFilter]
    search_fields = ['username', 'email', 'role', 'status']
    
    def get_queryset(self):
        return UserOrganization.objects.filter(status__in = ['active', 'inactive']).select_related('user').order_by('pk')


class UpdateOrganizationInternalView(generics.RetrieveUpdateAPIView):
    serializer_class = OrganizationInternalSerializer
    permission_classes = [custom_permissions.IsOrganizationInternal]
    lookup_field = 'username'
    filter_backends = [SearchFilter]
    search_fields = ['username', 'email', 'role', 'status']
    
    def get_object(self):
        return UserOrganization.objects.get(user__username=self.kwargs['username'], status__in=['active','inactive'])
    
class DeleteOrganizationInternalView(generics.DestroyAPIView):
    permission_classes = [custom_permissions.IsOrganizationInternal]
    lookup_field = 'username'
    filter_backends = [SearchFilter]
    search_fields = ['username', 'email', 'role', 'status']
    
    def get_object(self):
        return UserOrganization.objects.get(user__username=self.kwargs['username'], status__in = ['active', 'inactive'])
    
    def perform_destroy(self, instance):
        curr_user = UserOrganization.objects.get(user = self.request.user, status = StatusChoices.Active)
        curr_user_role = curr_user.role
        role_dict = {
            'owner': 1,
            'admin': 2,
            'manager': 3,
            'staff': 4
        }
        
        if role_dict[curr_user_role] >= role_dict[instance.role]:
            raise serializers.ValidationError('You do not have permission to delete this user')
        
        instance.role = ""
        instance.salary = 0
        instance.status = StatusChoices.Removed
        instance.save()
        
