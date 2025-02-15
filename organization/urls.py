from django.urls import path

from . import views

urlpatterns = [
    path('organizations/<slug:org_slug>/products/<slug:prod_slug>', views.RetrieveSpecificOrganizationProductView.as_view(), name='specific_organization_specific_product'),
    path('organizations/<slug:org_slug>/products', views.ListSpecificOrganizationProductView.as_view(), name='specific_organization_products'),
    path('organizations/<slug:org_slug>', views.RetrievePublicOrganizationView.as_view(), name='public_specific_organization'),
    path('organizations', views.ListPublicOrganizationView.as_view(), name='public_organizations'),
    path('we/internals/<uuid:uid>', views.RetrieveUpdateDeleteOrganizationInternalView.as_view(), name='update_organization_internal'),
    path('we/<uuid:uid>', views.RetrieveUpdateOrganizationView.as_view(), name='retrieve_update_organization'),
    path('we/internals', views.ListCreateOrganizationInternalView.as_view(), name='organization_internals'),
    path('we', views.ListMeOrganizationsView.as_view(), name='me_organization'),
    path('me/organization', views.CreateOrganizationView.as_view(), name='user_create_organization'),
    # path('we/internal/', views.CreateOrganizationInternalView.as_view(), name='create_organization_internal'),
    # path('we/delete-internal/<uuid:uid>', views.DeleteOrganizationInternalView.as_view(), name='delete_organization_internal'),
]