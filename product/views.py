from django.http import Http404
from rest_framework import generics

from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

from core.choices import ProductStatusChoices, StatusChoices
from core.models import MediaRoom, MediaRoomConnector, Product, UserOrganization 
from core import permissions as custom_permissions

from .serializers import MediaRoomSerializer, ProductSerializer, PublicProductSerializer 

# class CreateProductView(generics.CreateAPIView):
#     # queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#     permission_classes = [custom_permissions.IsOrganizationInternal]


class ListProductPublicView(generics.ListAPIView):
    queryset = (
        Product.objects.IS_PUBLISHED()
        .prefetch_related("category", "reviews")
        .select_related("organization")
        .order_by("pk")
    )
    serializer_class = PublicProductSerializer
    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    search_fields = ["name", "category__name", "description"]
    filterset_fields = ["availability", "brand"]
    ordering_fields = ["price", "avg_rating"]


# class ListSpecificOrganizationProductPublicView(generics.ListAPIView):
#     # queryset = Product.objects.filter(status = ProductStatusChoices.PUBLISHED).prefetch_related('category', 'reviews').order_by('pk')
#     serializer_class = PublicProductSerializer
#     lookup_field = 'slug'
#     filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
#     search_fields = ['name', 'category__name', 'description']
#     filterset_fields = ['availability', 'brand']
#     ordering_fields = ['price', 'avg_rating']

#     def get_queryset(self):
#         return Product.objects.filter(organization__slug=self.kwargs['slug'], status = ProductStatusChoices.PUBLISHED).prefetch_related('category', 'reviews').order_by('pk')


class ListCreateProductOrganizationInternalView(generics.ListCreateAPIView):
    # queryset = Product.objects.filter().order_by('pk').prefetch_related('category')
    # permission_classes = [custom_permissions.IsOrganizationInternal]
    serializer_class = ProductSerializer
    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    search_fields = ["name", "category__name", "description"]
    filterset_fields = ["availability", "brand"]
    ordering_fields = ["price", "avg_rating"]

    def get_permissions(self):
        if self.request.method == "POST":
            permission_classes = [custom_permissions.IsOrganizationManager]

        else:
            permission_classes = [custom_permissions.IsOrganizationStaff]

        return [permission() for permission in permission_classes]

    def get_queryset(self):
        user_orgs = UserOrganization.objects.IS_ACTIVE().filter(
            user=self.request.user
        ).values_list("organization", flat=True)
        return (
            Product.objects.filter(organization__in=user_orgs)
            .prefetch_related("category")
            .order_by("pk")
        )


class RetrieveProductPublicView(generics.RetrieveAPIView):
    serializer_class = PublicProductSerializer
    # lookup_field = 'slug'
    # filter_backends = [SearchFilter]
    # search_fields = ['name', 'category__name', 'description', 'price','availability', 'avg_rating', 'brand']

    def get_object(self):
        # slug = self.kwargs.get(self.lookup_field)
        org_slug = self.kwargs["org_slug"]
        prod_slug = self.kwargs["prod_slug"]
        return Product.objects.IS_PUBLISHED().get(
            slug=prod_slug,
            organization__slug=org_slug,
        )


class RetrieveUpdateDeleteProductView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProductSerializer
    permission_classes = [custom_permissions.IsOrganizationManager]
    lookup_field = "uid"
    # filter_backends = [SearchFilter]
    # search_fields = ['name', 'category__name', 'description', 'price','availability', 'avg_rating', 'brand']

    def get_object(self):
        # slug = self.kwargs.get(self.lookup_field)
        uid = self.kwargs["uid"]
        user_orgs = UserOrganization.objects.IS_ACTIVE().filter(
            user=self.request.user
        ).values_list("organization", flat=True)

        try:
            product = Product.objects.get(
                uid=uid, organization__in=user_orgs, status__in=["PUBLISHED", "DRAFT"]
            )

        except Product.DoesNotExist:
            raise Http404("Product does not exist")

        return product
        # return Product.objects.get(uid = uid, organization__in=user_orgs, status__in=['PUBLISHED', 'DRAFT'])

    def perform_destroy(self, instance):
        instance.status = ProductStatusChoices.REMOVED
        instance.save()


class ListCreateProductImageView(generics.ListCreateAPIView):
    serializer_class = MediaRoomSerializer
    permission_classes = [custom_permissions.IsOrganizationManager]
    lookup_field = "uid"

    def get_queryset(self):
        # slug = self.kwargs.get(self.lookup_field)
        uid = self.kwargs["uid"]
        user_orgs = UserOrganization.objects.IS_ACTIVE().filter(
            user=self.request.user
        ).values_list("organization", flat=True)

        try:
            product = Product.objects.get(
                uid=uid, organization__in=user_orgs, status__in=["PUBLISHED", "DRAFT"]
            )
        except Product.DoesNotExist:
            raise Http404("Product does not exist")

        medias = MediaRoomConnector.objects.filter(product=product)

        return MediaRoom.objects.filter(id__in=medias)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["prod_uid"] = self.kwargs["uid"]
        return context
