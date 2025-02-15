from rest_framework import generics, permissions, serializers

from rest_framework.filters import OrderingFilter, SearchFilter

from django_filters.rest_framework import DjangoFilterBackend

from django.core.exceptions import PermissionDenied


from core.choices import ProductStatusChoices, StatusChoices
from core.models import Organization, Product, UserOrganization
from core import permissions as custom_permissions

from .serializers import (
    OrganizationInternalDetailsSerializer,
    OrganizationInternalSerializer,
    OrganizationSerializer,
    PublicOrganizationSerializer,
)

from product.serializers import PublicProductSerializer


class CreateOrganizationView(generics.CreateAPIView):
    serializer_class = OrganizationSerializer
    permission_classes = [permissions.IsAuthenticated]


class ListMeOrganizationsView(generics.ListAPIView):
    # queryset = Organization.objects.filter(status=StatusChoices.ACTIVE).order_by('pk')
    permission_classes = [custom_permissions.IsOrganizationStaff]
    serializer_class = OrganizationSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ["name", "email", "description"]
    filterset_fields = ["thana", "city", "country"]
    ordering_fields = ["date_joined", "updated_at"]

    def get_queryset(self):
        user = self.request.user

        organizations = UserOrganization.objects.IS_ACTIVE().filter(user=user).values_list("organization", flat=True)

        return Organization.objects.filter(id__in=organizations).order_by("pk")


class RetrieveUpdateOrganizationView(generics.RetrieveUpdateAPIView):
    serializer_class = OrganizationSerializer
    lookup_field = "uid"

    def get_permissions(self):
        if self.request.method == "GET":
            permission_classes = [custom_permissions.IsOrganizationStaff]

        else:
            permission_classes = [custom_permissions.IsOrganizationOwner]

        return [permission() for permission in permission_classes]

    def get_object(self):
        org = Organization.objects.get(uid=self.kwargs["uid"])
        if not UserOrganization.objects.filter(
            user=self.request.user, organization=org
        ).exists():
            raise PermissionDenied(
                "You are not authorized to perform this action on this organization."
            )

        return org


class ListPublicOrganizationView(generics.ListAPIView):
    # queryset = Organization.objects.filter(status=StatusChoices.ACTIVE).order_by("pk")
    queryset = Organization.objects.IS_ACTIVE().order_by("pk")
    serializer_class = PublicOrganizationSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ["name", "email", "description"]
    filterset_fields = ["thana", "city", "country"]


class RetrievePublicOrganizationView(generics.RetrieveAPIView):
    # queryset = Organization.objects.filter(status = StatusChoices.ACTIVE).order_by('pk')
    serializer_class = PublicOrganizationSerializer
    lookup_field = "slug"

    def get_object(self):
        return Organization.objects.IS_ACTIVE().get(slug=self.kwargs["org_slug"])


class ListSpecificOrganizationProductView(generics.ListAPIView):
    serializer_class = PublicProductSerializer
    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    search_fields = ["name", "category__name", "description"]
    filterset_fields = ["availability", "brand"]
    ordering_fields = ["price", "avg_rating"]

    def get_queryset(self):
        org = Organization.objects.IS_ACTIVE().get(slug=self.kwargs["org_slug"])

        return Product.objects.IS_PUBLISHED().filter(
            organization=org
        ).order_by("pk")


class RetrieveSpecificOrganizationProductView(generics.RetrieveAPIView):
    serializer_class = PublicProductSerializer

    def get_object(self):
        org = Organization.objects.IS_ACTIVE().get(slug=self.kwargs["org_slug"])

        return Product.objects.IS_PUBLISHED().get(
            slug=self.kwargs["prod_slug"],
            organization=org,
        )


# class ListMeOrganizationInternalMembersView(generics.ListAPIView):
#     serializer_class = UserOrganizationSerializer
#     permission_classes = [custom_permissions.IsOrganizationInternal]
#     filter_backends = [SearchFilter]
#     search_fields = ['username', 'role', 'status']


#     def get_queryset(self):
#         return UserOrganization.objects.filter(status__in = ['active', 'inactive']).select_related('user').order_by('pk')


# class CreateOrganizationInternalView(generics.CreateAPIView):
#     serializer_class = OrganizationInternalSerializer
#     permission_classes = [custom_permissions.IsOrganizationManager]
#     filter_backends = [SearchFilter]
#     search_fields = ['username', 'email', 'organization', 'role', 'status']


class ListCreateOrganizationInternalView(generics.ListCreateAPIView):
    # serializer_class = OrganizationInternalDetailsSerializer
    permission_classes = [custom_permissions.IsOrganizationStaff]
    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    search_fields = ["user__username", "organization__name", "user__email"]
    filterset_fields = ["role", "status"]
    ordering_fields = ["salary"]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return OrganizationInternalSerializer
        return OrganizationInternalDetailsSerializer

    def get_queryset(self):
        user_organizations = UserOrganization.objects.IS_ACTIVE().filter(
            user=self.request.user
        ).values_list("organization", flat=True)
        return (
            UserOrganization.objects.filter(organization__in=user_organizations)
            .select_related("user")
            .prefetch_related("organization")
            .order_by("pk")
        )


class RetrieveUpdateDeleteOrganizationInternalView(
    generics.RetrieveUpdateDestroyAPIView
):
    serializer_class = OrganizationInternalSerializer
    permission_classes = [custom_permissions.IsOrganizationManager]
    lookup_field = "uid"
    # filter_backends = [SearchFilter]
    # search_fields = ['username', 'email', 'role', 'status']

    def get_object(self):
        return UserOrganization.objects.get(
            uid=self.kwargs["uid"], status__in=["ACTIVE", "INACTIVE"]
        )

    def perform_destroy(self, instance):
        curr_user = UserOrganization.objects.IS_ACTIVE().get(
            user=self.request.user
        )
        curr_user_role = curr_user.role
        role_dict = {"owner": 1, "admin": 2, "manager": 3, "staff": 4}

        if (
            role_dict[curr_user_role.lower()] >= role_dict[instance.role.lower()]
            or curr_user.organization != instance.organization
        ):
            raise serializers.ValidationError(
                "You do not have permission to delete this user"
            )

        instance.role = ""
        instance.salary = 0
        instance.status = StatusChoices.REMOVED
        instance.save()


# class DeleteOrganizationInternalView(generics.DestroyAPIView):
#     permission_classes = [custom_permissions.IsOrganizationManager]
#     lookup_field = 'uid'
#     filter_backends = [SearchFilter]
#     search_fields = ['username', 'email', 'role', 'status']

#     def get_object(self):
#         return UserOrganization.objects.get(uid=self.kwargs['uid'], status__in = ['ACTIVE', 'INACTIVE'])

#     def perform_destroy(self, instance):
#         curr_user = UserOrganization.objects.get(user = self.request.user, status = StatusChoices.ACTIVE)
#         curr_user_role = curr_user.role
#         role_dict = {
#             'owner': 1,
#             'admin': 2,
#             'manager': 3,
#             'staff': 4
#         }


#         if role_dict[curr_user_role.lower()] >= role_dict[instance.role.lower()] or curr_user.organization != instance.organization:
#             raise serializers.ValidationError('You do not have permission to delete this user')

#         instance.role = ""
#         instance.salary = 0
#         instance.status = StatusChoices.REMOVED
#         instance.save()
