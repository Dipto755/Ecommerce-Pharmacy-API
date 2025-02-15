from django.urls import path

from . import views

urlpatterns = [
    # path('we/product/add', views.CreateProductView.as_view(), name='create_product'),
    path('we/products/<uuid:uid>/images', views.ListCreateProductImageView.as_view(), name='list_create_product_image'),
    path('we/products/<uuid:uid>', views.RetrieveUpdateDeleteProductView.as_view(), name='retrieve_update_delete_product'),
    path('we/products', views.ListCreateProductOrganizationInternalView.as_view(), name='list_create_product_organization_internal'),
    path('products', views.ListProductPublicView.as_view(), name='list_product_public'),
    # path('products/<slug:slug>', views.ListSpecificOrganizationProductPublicView.as_view(), name='list_organization_product_public'),
    # path('product/<slug:org_slug>/<slug:prod_slug>', views.RetrieveProductPublicView.as_view(), name='retrieve_product_public'),
]