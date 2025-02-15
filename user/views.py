from rest_framework import generics
from rest_framework import permissions as drf_permissions

from rest_framework.filters import SearchFilter

from core.models import User
from core.choices import StatusChoices
from core import permissions as custom_permissions

from .serializers import UserSerializer, UserOrganizationSerializer


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer

class GetAllUserView(generics.ListAPIView):
    queryset = User.objects.filter(status = StatusChoices.Active).order_by('pk')
    serializer_class = UserSerializer
    permission_classes = [custom_permissions.IsSuperuser]
    filter_backends = [SearchFilter]
    search_fields = ['username', 'first_name', 'last_name', 'thana', 'city', 'country', 'status']
    
    
    
class GetAndUpdateMeUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [drf_permissions.IsAuthenticated]
    
    def get_object(self):
        """Retrieve and return authenticated user"""
        return self.request.user


class CreateOrganizationUserView(generics.CreateAPIView):
    serializer_class = UserOrganizationSerializer
    permission_classes = [custom_permissions.IsSuperuser]

