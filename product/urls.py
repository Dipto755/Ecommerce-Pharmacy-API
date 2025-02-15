from django.urls import path

from . import views

urlpatterns = [
    path('we/product/add', views.CreateProductView.as_view(), name='create_product'),
    path('products', views.ListProductPublicView.as_view(), name='list_product_public'),
    path('we/products', views.ListProductOrganizationInternalView.as_view(), name='list_product_organization_internal'),
    path('product/<str:slug>', views.RetrieveProductPublicView.as_view(), name='retrieve_product_public'),
    path('we/product/update/<str:slug>', views.RetrieveUpdateProductView.as_view(), name='update_product'),
]