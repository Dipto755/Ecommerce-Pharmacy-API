from django.urls import path

from . import views

urlpatterns = [
    path('we/internals', views.ListOrganizationInternalView.as_view(), name='organization_internals'),
    path('we/internal/', views.CreateOrganizationInternalView.as_view(), name='organization_internals'),
    path('we/update-internal/<str:username>', views.UpdateOrganizationInternalView.as_view(), name='update_organization_internal'),
    path('we/delete-internal/<str:username>', views.DeleteOrganizationInternalView.as_view(), name='delete_organization_internal'),
]