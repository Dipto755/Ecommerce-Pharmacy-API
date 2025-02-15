from rest_framework import generics

from rest_framework.filters import SearchFilter

from core.choices import ProductStatusChoices
from core.models import Product
from core import permissions as custom_permissions

from .serializers import ProductSerializer, PublicProductSerializer

class CreateProductView(generics.CreateAPIView):
    # queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [custom_permissions.IsOrganizationInternal]
    
class ListProductPublicView(generics.ListAPIView):
    queryset = Product.objects.filter(status = ProductStatusChoices.Published).prefetch_related('category', 'reviews').order_by('pk')
    serializer_class = PublicProductSerializer
    filter_backends = [SearchFilter]
    search_fields = ['name', 'category', 'description', 'price','availability', 'avg_rating', 'brand']
    
    
class ListProductOrganizationInternalView(generics.ListAPIView):
    queryset = Product.objects.filter().order_by('pk').prefetch_related('category')
    permission_classes = [custom_permissions.IsOrganizationInternal]
    serializer_class = ProductSerializer
    filter_backends = [SearchFilter]
    search_fields = ['name', 'category', 'description', 'price','availability', 'avg_rating', 'brand']

class RetrieveProductPublicView(generics.RetrieveAPIView):
    serializer_class = PublicProductSerializer
    lookup_field = 'slug'
    filter_backends = [SearchFilter]
    search_fields = ['name', 'category', 'description', 'price','availability', 'avg_rating', 'brand']
    
    def get_object(self):
        slug = self.kwargs.get(self.lookup_field)
        return Product.objects.get(slug = slug, status = ProductStatusChoices.Published)
    
class RetrieveUpdateProductView(generics.RetrieveUpdateAPIView):
    serializer_class = ProductSerializer
    permission_classes = [custom_permissions.IsOrganizationManager]
    lookup_field = 'slug'
    filter_backends = [SearchFilter]
    search_fields = ['name', 'category', 'description', 'price','availability', 'avg_rating', 'brand']
    
    def get_object(self):
        slug = self.kwargs.get(self.lookup_field)
        return Product.objects.get(slug = slug)

    