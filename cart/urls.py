from django.urls import path
from . import views

urlpatterns = [
    # path('me/cart', views.ListMeCartView.as_view(), name='me_cart'),
    path('me/cart/items/<uuid:uid>', views.RetrieveUpdateRemoveCartItemView.as_view(), name='remove_cart_item'),
    path('me/cart/items', views.ListCreateCartItemsView.as_view(), name='me_cart_items'),
    path('me/cart', views.RetrieveMeCartView.as_view(), name='me_cart_details'),
    # path('me/cart/add-items/', views.AddCartItemView.as_view(), name='add_cartitems'),
    # path('me/order/add-order', views.AddOrderView.as_view(), name='add_order'),
    path('me/orders/<uuid:order_uid>/items/<uuid:item_uid>', views.RetrieveRemoveOrderItemView.as_view(), name='retrieve_remove_order_item'),
    # path('me/orders/delivered/<uuid:order_uid>/review/<uuid:review_uid>/images', views.AddReviewView.as_view(), name='add_review'),
    path('me/orders/delivered/<uuid:order_uid>/review', views.AddReviewView.as_view(), name='add_review'),
    path('me/orders/delivered/<uuid:order_uid>', views.RetrieveMeDeliveredOrderView.as_view(), name='me_specific_delivered_order'),
    path('me/orders/<uuid:uid>', views.OrderDetailsView.as_view(), name='my_order_details'),
    path('me/orders/delivered', views.ListMeDeliveredOrdersView.as_view(), name='my_delivered_orders'),
    path('me/order', views.AddOrderItemView.as_view(), name='add_order_items'),
    path('me/orders', views.ListMeOrderView.as_view(), name='my_orders'),
    path('me/reviews/<uuid:uid>/images', views.ListCreateReviewImageView.as_view(), name='list_create_review_image'),
    path('me/reviews', views.MyReviewDetailsView.as_view(), name='my_reviews'),
    path('we/orders/<uuid:uid>', views.RetrieveUpdateOrderView.as_view(), name='update_order'),
    path('we/orders', views.GetAllOrders.as_view(), name='all_orders'),
    # path('we/orders/<uuid:uid>', views.RetrieveUpdateOrderView.as_view(), name='update_order'),
    
]